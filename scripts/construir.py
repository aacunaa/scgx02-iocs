"""Genera los feeds, el paquete STIX 2.1 y la tabla legible a partir de datos/iocs.csv.

    python scripts/construir.py              escribe feeds/, un paquete STIX por campaña en stix/ e IOCS.md
    python scripts/construir.py --comprobar  falla si lo generado no coincide con lo que está en el repositorio (lo usa la integración continua)

Solo biblioteca estándar. Todo es determinista: el mismo CSV da los mismos archivos, byte a byte, con los mismos identificadores STIX.
Antes de escribir, valida cada fila y, si existe el archivo local `.denylist` (no se sube: está en .gitignore), rechaza cualquier valor que contenga
uno de sus términos. Ahí van los nombres de víctimas y de empresas afectadas, que nunca deben publicarse.
Cada fila pertenece a una campaña de CAMPANAS. Los feeds juntan todas (sirven para bloquear); STIX y la tabla las separan.
"""
from __future__ import annotations

import csv
import ipaddress
import json
import os
import re
import sys
import uuid

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(RAIZ, "datos", "iocs.csv")
DENYLIST = os.environ.get("IOC_DENYLIST", os.path.join(RAIZ, ".denylist"))
NS = uuid.UUID("5c7e2b8e-3f0a-4d0e-9d55-2a7c1b9e0f42")          # espacio fijo: los mismos valores dan los mismos identificadores STIX

COLUMNAS = ["campana", "tipo", "valor", "rol", "confianza", "visto_primero", "estado", "estado_al", "notas"]
TIPOS = {"dominio", "host", "url", "sha256", "md5", "x509-sha256", "cadena", "ipv4"}
ESTADOS = {"", "activo", "caido", "bloqueado", "preparado", "sin_datos"}
CONFIANZA = {"alta": 85, "media": 60, "baja": 30}
NOMBRE_DNS = re.compile(r"^(?=.{1,253}$)([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$")
FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FORMATOS = {"sha256": re.compile(r"^[0-9a-f]{64}$"), "x509-sha256": re.compile(r"^[0-9a-f]{64}$"), "md5": re.compile(r"^[0-9a-f]{32}$")}
# Servicios legítimos que el actor usa como alojamiento: se publica el host del actor, nunca el dominio del servicio.
SERVICIOS = ("myqcloud.com", "amazonaws.com", "linodeobjects.com", "windows.net", "flyn.co")

TLP_WHITE = {"type": "marking-definition", "spec_version": "2.1", "id": "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9",
             "created": "2017-01-20T00:00:00.000Z", "definition_type": "tlp", "name": "TLP:WHITE", "definition": {"tlp": "white"}}
IDENTIDAD = "identity--" + str(uuid.uuid5(NS, "Raiku Solutions"))
# Una entrada por campaña. El identificador STIX sale del nombre: no cambiar el nombre de una campaña ya publicada.
CAMPANAS = {
    "scgx02": {
        "nombre": "SCGX02 / CodeStorm", "stix": "stix/scgx02.json",
        "descripcion": "Phishing de adversario en el medio (AiTM) contra cuentas de Microsoft 365, entregado desde cuentas reales de proveedores comprometidos. "
                       "Kit con panel «SCGX02 PANEL», landings detrás de Cloudflare y la interfaz de phishing en buckets de Tencent Cloud."},
    "rfq-aitm": {
        "nombre": "RFQ en dos pasos / proxy AiTM", "stix": "stix/rfq-aitm.json",
        "descripcion": "Falsas solicitudes de cotización en dos pasos: un primer correo sin enlaces desde buzones reales comprometidos y, cuando la víctima "
                       "responde, la continuación desde un dominio que suplanta a una empresa real, con un enlace que pasa por una redirección OAuth abierta. "
                       "Termina en un proxy AiTM del inicio de sesión de Microsoft, detrás de una puerta con prueba de trabajo, huella del navegador, "
                       "detector de entornos de análisis y captcha propio."},
}


class FilaInvalida(ValueError):
    pass


def cargar(ruta: str = CSV) -> list[dict]:
    with open(ruta, encoding="utf-8", newline="") as fh:
        lector = csv.DictReader(fh)
        if lector.fieldnames != COLUMNAS:
            raise FilaInvalida(f"columnas esperadas {COLUMNAS}, encontradas {lector.fieldnames}")
        return [dict(f) for f in lector]


def terminos_prohibidos(ruta: str = DENYLIST) -> list[str]:
    if not os.path.exists(ruta):
        return []
    with open(ruta, encoding="utf-8") as fh:
        return [t.strip().lower() for t in fh if t.strip() and not t.startswith("#")]


def validar(filas: list[dict], prohibidos: list[str] = ()) -> None:
    """Lanza FilaInvalida con todos los problemas juntos."""
    errores, vistos = [], set()
    for n, f in enumerate(filas, start=2):
        t, v = f["tipo"], f["valor"]
        if f["campana"] not in CAMPANAS:
            errores.append(f"línea {n}: campaña desconocida «{f['campana']}» ({', '.join(CAMPANAS)})")
        if t not in TIPOS:
            errores.append(f"línea {n}: tipo desconocido «{t}»")
            continue
        comparable = v.split("://", 1)[-1].split("/", 1)[0] if t == "url" else v          # en una URL solo el host va en minúsculas: la ruta distingue mayúsculas
        if v != v.strip() or (t != "cadena" and comparable != comparable.lower()):
            errores.append(f"línea {n}: «{v}» debe ir sin espacios y en minúsculas")
        if (t, v) in vistos:
            errores.append(f"línea {n}: «{v}» repetido")
        vistos.add((t, v))
        if t in ("dominio", "host") and not NOMBRE_DNS.match(v):
            errores.append(f"línea {n}: «{v}» no es un nombre de dominio")
        if t == "dominio" and v.endswith(SERVICIOS):
            errores.append(f"línea {n}: «{v}» es un servicio legítimo: va como host, no como dominio")
        if t == "url" and not re.match(r"^https?://[^\s/]+", v):
            errores.append(f"línea {n}: «{v}» no es una URL")
        if t in FORMATOS and not FORMATOS[t].match(v):
            errores.append(f"línea {n}: «{v}» no tiene el formato de {t}")
        if t == "ipv4":
            try:
                ip = ipaddress.ip_address(v)
                if not ip.is_global:
                    errores.append(f"línea {n}: «{v}» no es una dirección pública")
            except ValueError:
                errores.append(f"línea {n}: «{v}» no es una dirección IPv4")
        if f["confianza"] not in CONFIANZA:
            errores.append(f"línea {n}: confianza «{f['confianza']}» (alta, media o baja)")
        if f["estado"] not in ESTADOS:
            errores.append(f"línea {n}: estado «{f['estado']}»")
        for col in ("visto_primero", "estado_al"):
            if f[col] and not FECHA.match(f[col]):
                errores.append(f"línea {n}: {col} «{f[col]}» no es AAAA-MM-DD")
        if not f["visto_primero"] or not f["rol"]:
            errores.append(f"línea {n}: faltan el rol o la fecha")
        texto = " ".join(f.values()).lower()
        for p in prohibidos:
            if p in texto:
                errores.append(f"línea {n}: contiene un término de .denylist (no se muestra cuál)")
    if errores:
        raise FilaInvalida("\n".join(errores))


def desarmar(t: str, v: str) -> str:
    """El valor sin peligro de clic para leerlo en un documento (hxxp, [.])."""
    if t == "url":
        v = v.replace("https://", "hxxps://").replace("http://", "hxxp://")
        esquema, resto = v.split("://", 1)
        host, _, ruta = resto.partition("/")
        return f"{esquema}://{host.replace('.', '[.]')}" + (f"/{ruta}" if ruta else "")
    if t in ("dominio", "host", "ipv4"):
        return v.replace(".", "[.]")
    return v


def _patron(t: str, v: str) -> str | None:
    lit = v.replace("\\", "\\\\").replace("'", "\\'")
    return {"dominio": f"[domain-name:value = '{lit}']", "host": f"[domain-name:value = '{lit}']", "url": f"[url:value = '{lit}']",
            "ipv4": f"[ipv4-addr:value = '{lit}']", "sha256": f"[file:hashes.'SHA-256' = '{lit}']", "md5": f"[file:hashes.MD5 = '{lit}']",
            "x509-sha256": f"[x509-certificate:hashes.'SHA-256' = '{lit}']"}.get(t)


def version(filas: list[dict]) -> str:
    return max(f["estado_al"] or f["visto_primero"] for f in filas)


def stix(filas: list[dict], clave: str) -> dict:
    """El paquete de una campaña: solo sus filas."""
    camp = CAMPANAS[clave]
    filas = [f for f in filas if f["campana"] == clave]
    id_camp = "campaign--" + str(uuid.uuid5(NS, camp["nombre"]))
    ts = version(filas) + "T00:00:00.000Z"
    base = {"spec_version": "2.1", "created": ts, "modified": ts, "created_by_ref": IDENTIDAD, "object_marking_refs": [TLP_WHITE["id"]]}
    objetos = [TLP_WHITE,
               {"type": "identity", "spec_version": "2.1", "id": IDENTIDAD, "created": ts, "modified": ts, "name": "Raiku Solutions", "identity_class": "organization",
                "sectors": ["technology"], "object_marking_refs": [TLP_WHITE["id"]]},
               {"type": "campaign", "id": id_camp, **base, "name": camp["nombre"], "description": camp["descripcion"],
                "first_seen": min(f["visto_primero"] for f in filas) + "T00:00:00.000Z"}]
    for f in filas:
        patron = _patron(f["tipo"], f["valor"])
        if not patron:
            continue
        ind = "indicator--" + str(uuid.uuid5(NS, f"{f['tipo']}|{f['valor']}"))
        objetos.append({"type": "indicator", "id": ind, **base, "name": f"{f['rol']}: {desarmar(f['tipo'], f['valor'])}",
                        "description": f["notas"] or f["rol"], "indicator_types": ["malicious-activity"], "pattern": patron, "pattern_type": "stix",
                        "valid_from": f["visto_primero"] + "T00:00:00.000Z", "confidence": CONFIANZA[f["confianza"]],
                        "labels": [f"estado:{f['estado']}"] if f["estado"] else []})
        objetos.append({"type": "relationship", "id": "relationship--" + str(uuid.uuid5(NS, ind + "|indicates")), **base,
                        "relationship_type": "indicates", "source_ref": ind, "target_ref": id_camp})
    return {"type": "bundle", "id": "bundle--" + str(uuid.uuid5(NS, clave + "|" + version(filas))), "objects": objetos}


def feeds(filas: list[dict]) -> dict[str, str]:
    """Un valor por línea, sin desarmar: son para cargar en un bloqueo o en un SIEM. La cabecera dice qué son."""
    v = version(filas)

    def lista(nombre, tipos, solo=None):
        valores = sorted({f["valor"] for f in filas if f["tipo"] in tipos and (solo is None or f["estado"] in solo)})
        cab = f"# {' + '.join(c['nombre'] for c in CAMPANAS.values())} — {nombre}. TLP:CLEAR. Versión {v}. Fuente: datos/iocs.csv. Un valor por línea.\n"
        return cab + "".join(x + "\n" for x in valores)
    return {"feeds/dominios.txt": lista("dominios y hosts del actor (bloquear también los subdominios de los dominios base)", ("dominio", "host")),
            "feeds/dominios_activos.txt": lista("dominios y hosts activos, preparados o bloqueados al " + v, ("dominio", "host"), {"activo", "preparado", "bloqueado"}),
            "feeds/urls.txt": lista("URLs", ("url",)),
            "feeds/sha256.txt": lista("hashes SHA-256 de archivos", ("sha256",)),
            "feeds/md5.txt": lista("hashes MD5 de archivos", ("md5",)),
            "feeds/x509-sha256.txt": lista("huellas SHA-256 de certificados", ("x509-sha256",))}


def tabla(filas: list[dict]) -> str:
    v = version(filas)
    nombres = {"dominio": "Dominios base", "host": "Hosts", "url": "URLs", "sha256": "Archivos (SHA-256)", "md5": "Archivos (MD5)",
               "x509-sha256": "Certificados (SHA-256)", "cadena": "Cadenas para cazar", "ipv4": "Direcciones IP"}
    l = [f"# IOC publicados por Raiku Solutions (versión {v})", "",
         "Tabla generada desde `datos/iocs.csv` con `scripts/construir.py`. Los valores están desarmados (`[.]`, `hxxps`) para que no se puedan abrir por error.",
         "Los valores tal cual, para cargar en un bloqueo, están en `feeds/` (todas las campañas juntas), y un paquete STIX 2.1 por campaña en `stix/`.", ""]
    for clave, camp in CAMPANAS.items():
        de_la_campana = [f for f in filas if f["campana"] == clave]
        if de_la_campana:
            l += [f"## {camp['nombre']} (versión {version(de_la_campana)}, `{camp['stix']}`)", ""] + _tabla_campana(de_la_campana, nombres)
    return "\n".join(l)


def _tabla_campana(filas: list[dict], nombres: dict[str, str]) -> list[str]:
    l = []
    for t in ("dominio", "host", "url", "sha256", "md5", "x509-sha256", "ipv4", "cadena"):
        grupo = [f for f in filas if f["tipo"] == t]
        if not grupo:
            continue
        l += [f"### {nombres[t]} ({len(grupo)})", "", "| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |", "|---|---|---|---|---|---|"]
        for f in sorted(grupo, key=lambda f: (f["estado"] != "activo", f["valor"])):
            est = f"{f['estado'].replace('_', ' ')} ({f['estado_al']})" if f["estado"] else "—"
            l.append(f"| `{desarmar(t, f['valor'])}` | {f['rol']} | {f['confianza']} | {f['visto_primero']} | {est} | {f['notas'].replace('|', '/')} |")
        l.append("")
    return l


def generar(filas: list[dict]) -> dict[str, str]:
    out = feeds(filas)
    for clave, camp in CAMPANAS.items():
        if any(f["campana"] == clave for f in filas):
            out[camp["stix"]] = json.dumps(stix(filas, clave), ensure_ascii=False, indent=1) + "\n"
    out["IOCS.md"] = tabla(filas)
    return out


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    filas = cargar()
    try:
        validar(filas, terminos_prohibidos())
    except FilaInvalida as e:
        print(f"datos/iocs.csv tiene problemas:\n{e}", file=sys.stderr)
        return 1
    archivos = generar(filas)
    if "--comprobar" in argv:
        viejos = []
        for ruta, contenido in archivos.items():
            p = os.path.join(RAIZ, ruta)
            if not os.path.exists(p):
                viejos.append(ruta)
                continue
            with open(p, encoding="utf-8", newline="") as fh:
                if fh.read() != contenido:
                    viejos.append(ruta)
        if viejos:
            print("Desactualizados (correr scripts/construir.py): " + ", ".join(viejos), file=sys.stderr)
            return 1
        print(f"OK: {len(filas)} IOC, archivos al día")
        return 0
    for ruta, contenido in archivos.items():
        p = os.path.join(RAIZ, ruta)
        os.makedirs(os.path.dirname(p) or RAIZ, exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(contenido)
    print(f"{len(filas)} IOC: " + ", ".join(sorted(archivos)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
