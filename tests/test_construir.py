"""Pruebas del generador y de los datos publicados.   python -m unittest discover -s tests"""
import json
import os
import re
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
import construir as C  # noqa: E402


def fila(**kw):
    base = {"tipo": "dominio", "valor": "ejemplo-malo.de", "rol": "dominio base", "confianza": "alta", "visto_primero": "2026-10-16", "estado": "activo",
            "estado_al": "2026-11-01", "notas": ""}
    base.update(kw)
    return base


class LaValidacion(unittest.TestCase):
    def falla(self, filas, texto, prohibidos=()):
        with self.assertRaises(C.FilaInvalida) as cm:
            C.validar(filas, prohibidos)
        self.assertIn(texto, str(cm.exception))

    def test_los_datos_del_repositorio_son_validos(self):
        C.validar(C.cargar(), C.terminos_prohibidos())

    def test_rechaza_formatos_malos(self):
        self.falla([fila(valor="no es dominio")], "no es un nombre de dominio")
        self.falla([fila(tipo="sha256", valor="abc")], "no tiene el formato")
        self.falla([fila(tipo="url", valor="ftp//x")], "no es una URL")
        self.falla([fila(tipo="ipv4", valor="10.0.0.1")], "no es una dirección pública")
        self.falla([fila(confianza="total")], "confianza")
        self.falla([fila(visto_primero="16-10-2026")], "AAAA-MM-DD")
        self.falla([fila(valor="Mayus.de")], "minúsculas")

    def test_en_una_url_la_ruta_puede_tener_mayusculas_pero_el_host_no(self):
        C.validar([fila(tipo="url", valor="https://acortador.example/AbCd")])
        self.falla([fila(tipo="url", valor="https://Acortador.example/AbCd")], "minúsculas")

    def test_rechaza_repetidos_y_servicios_legitimos_como_dominio(self):
        self.falla([fila(), fila()], "repetido")
        self.falla([fila(valor="bucket-1.cos.na-siliconvalley.myqcloud.com")], "servicio legítimo")

    def test_un_termino_de_la_denylist_bloquea_y_no_se_muestra(self):
        with self.assertRaises(C.FilaInvalida) as cm:
            C.validar([fila(valor="victima.ejemplo-malo.de", tipo="host")], ["victima"])
        self.assertNotIn("victima", str(cm.exception))
        self.assertIn(".denylist", str(cm.exception))


class LoGenerado(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filas = C.cargar()
        cls.archivos = C.generar(cls.filas)
        cls.bundle = json.loads(cls.archivos["stix/scgx02.json"])

    def test_es_determinista(self):
        self.assertEqual(C.generar(C.cargar()), self.archivos)

    def test_lo_del_repositorio_esta_al_dia(self):
        self.assertEqual(C.main(["--comprobar"]), 0)

    def test_stix_ids_unicos_y_referencias_resueltas(self):
        objs = self.bundle["objects"]
        ids = [o["id"] for o in objs]
        self.assertEqual(len(ids), len(set(ids)))
        for o in objs:
            for k in ("created_by_ref", "source_ref", "target_ref"):
                if k in o:
                    self.assertIn(o[k], ids)
            for m in o.get("object_marking_refs", []):
                self.assertIn(m, ids)

    def test_stix_un_indicador_por_cada_ioc_con_patron(self):
        con_patron = [f for f in self.filas if f["tipo"] != "cadena"]
        indicadores = [o for o in self.bundle["objects"] if o["type"] == "indicator"]
        self.assertEqual(len(indicadores), len(con_patron))
        for o in indicadores:
            self.assertRegex(o["pattern"], r"^\[(domain-name|url|ipv4-addr|file|x509-certificate):")
            self.assertEqual(o["spec_version"], "2.1")
            self.assertIn(o["confidence"], (30, 60, 85))

    def test_los_feeds_tienen_valores_sin_desarmar(self):
        for ruta in ("feeds/dominios.txt", "feeds/urls.txt"):
            for linea in self.archivos[ruta].splitlines()[1:]:
                self.assertNotIn("[.]", linea)
                self.assertFalse(linea.startswith("hxxp"))

    def test_la_tabla_no_tiene_valores_que_se_puedan_abrir(self):
        for v in re.findall(r"`([^`]+)`", self.archivos["IOCS.md"]):
            if "." in v and not re.fullmatch(r"[0-9a-f.]+", v) and "/" not in v[:8]:
                self.assertIn("[.]", v, v)
        self.assertNotIn("https://", self.archivos["IOCS.md"])

    def test_desarmar(self):
        self.assertEqual(C.desarmar("url", "https://a.b.de/x.php?y=1"), "hxxps://a[.]b[.]de/x.php?y=1")
        self.assertEqual(C.desarmar("host", "a.b.de"), "a[.]b[.]de")
        self.assertEqual(C.desarmar("sha256", "ab"), "ab")


class LoQueNoSePublica(unittest.TestCase):
    def test_ningun_archivo_del_repositorio_contiene_terminos_de_la_denylist(self):
        prohibidos = C.terminos_prohibidos()
        if not prohibidos:
            self.skipTest("sin .denylist local (es lo normal fuera del equipo que mantiene el repositorio)")
        for carpeta, _, archivos in os.walk(RAIZ):
            if ".git" in carpeta.split(os.sep) or "__pycache__" in carpeta:
                continue
            for a in archivos:
                if a == ".denylist":
                    continue
                with open(os.path.join(carpeta, a), encoding="utf-8", errors="ignore") as fh:
                    texto = fh.read().lower()
                for p in prohibidos:
                    self.assertNotIn(p, texto, f"{a} contiene un término prohibido")

    def test_las_reglas_yara_compilan_y_detectan_el_panel(self):
        try:
            import yara
        except ImportError:
            self.skipTest("yara-python no está instalado (pip install yara-python)")
        reglas = yara.compile(filepath=os.path.join(RAIZ, "yara", "scgx02.yar"))
        self.assertEqual(len(list(reglas)), 5)
        panel = b"<html><head><title>Login Page</title></head><body><h1>SCGX02 PANEL</h1></body></html>"
        self.assertEqual([m.rule for m in reglas.match(data=panel)], ["PHISH_Kit_SCGX02_Panel"])
        self.assertEqual(reglas.match(data=b"%PDF-1.7 " + b"x" * 2000), [])

    def test_las_reglas_yara_estan_balanceadas(self):
        with open(os.path.join(RAIZ, "yara", "scgx02.yar"), encoding="utf-8") as fh:
            texto = fh.read()
        self.assertEqual(texto.count("{"), texto.count("}"))
        self.assertEqual(len(re.findall(r"^rule \w+", texto, re.M)), 5)


if __name__ == "__main__":
    unittest.main()
