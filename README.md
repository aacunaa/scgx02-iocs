# IOC de campañas de phishing AiTM — Raiku Solutions

Indicadores de compromiso de campañas de **phishing de adversario en el medio (AiTM)** contra cuentas de Microsoft 365. Los publica **Raiku Solutions** a partir de investigaciones de respuesta a incidentes en Chile (octubre y noviembre de 2026). **TLP:CLEAR:** se pueden compartir sin restricción.

| Campaña | Desde | STIX | YARA |
|---|---|---|---|
| **SCGX02 / CodeStorm** | octubre de 2026 | [`stix/scgx02.json`](stix/scgx02.json) | [`yara/scgx02.yar`](yara/scgx02.yar) |
| **RFQ en dos pasos / proxy AiTM** | noviembre de 2026 | [`stix/rfq-aitm.json`](stix/rfq-aitm.json) | [`yara/rfq-aitm.yar`](yara/rfq-aitm.yar) |
| **Mirai «wraith» / murrezbots** (botnet relacionada) | mayo de 2026 | [`stix/mirai-wraith.json`](stix/mirai-wraith.json) | — |

El repositorio nació con SCGX02, de ahí su nombre.

*English summary below.*

## SCGX02 / CodeStorm en cinco líneas

1. **Entrega:** el correo llega desde la cuenta real de un proveedor comprometido, así que pasa SPF, DKIM y DMARC. El señuelo es una invitación a licitar con un PDF cifrado de una página: una imagen y un enlace oculto.
2. **Landing:** el enlace lleva a un subdominio con el nombre de la víctima, bajo un dominio base del actor detrás de Cloudflare. Hay un control anti-bots propio («Secure Access Check») o Turnstile.
3. **Robo:** la interfaz de phishing (etapa 3) se carga desde buckets de Tencent Cloud y reenvía usuario, contraseña y segundo factor en tiempo real al panel del operador.
4. **Panel:** el panel «SCGX02 PANEL» se publica en `/panel/` de un host con nombre corto y número (`pierce16`, `quill99`, `vault53`…). Todos sirven el mismo HTML: SHA-256 `204a6074…`.
5. **Después:** inicios de sesión desde la infraestructura del kit y reglas de bandeja que esconden avisos.

## RFQ en dos pasos / proxy AiTM en cinco líneas

1. **Primer contacto:** una solicitud de cotización **sin enlaces ni adjuntos** desde el buzón real de una empresa comprometida. No hay nada que un filtro pueda marcar; solo busca una respuesta.
2. **Continuación:** cuando la víctima responde, llega un «Re:» desde un dominio que suplanta a una empresa real (con DKIM propio, así que pasa la autenticación), con un enlace «RFQ».
3. **Redirección:** el enlace empieza en el endpoint `/oauth/authorize` de un sitio legítimo, que con `prompt=none&id_token_hint=dummy` devuelve error y redirige igual al `redirect_uri` del actor, alojado en un sitio comprometido.
4. **Puerta:** `yizhaojingyun[.]com` decide quién ve el phishing: prueba de trabajo y huella del navegador (`/.verify`), detector de entornos de análisis (`/.detect`), captcha propio (`greenproxysimpleserver[.]cc`) y una trampa para las herramientas de desarrollo (`/.devtools`). A los bots los manda a Stack Overflow o a Google.
5. **Robo:** un proxy AiTM (`tfgevds.`, `loginlive.` y `loginms.yizhaojingyun[.]com`) reenvía en tiempo real el inicio de sesión de Microsoft y se queda con la sesión aunque haya segundo factor. La misma puerta atiende a otras campañas: es phishing como servicio.

### La plataforma detrás: «Green Proxy»

**Análisis completo:** [raiku.cl/research/green-proxy](https://raiku.cl/research/green-proxy) (inglés) · [versión en español](https://raiku.cl/research/green-proxy-es).

La raíz del dominio del captcha, `greenproxysimpleserver[.]cc`, es el **panel de clientes de una plataforma de phishing como servicio llamada «Green Proxy»**. Pide usuario, contraseña y una **licencia `GPKEY-XXXX-XXXX-XXXX`** y permite crear cuentas: el kit se arrienda. Quien envía los correos es probablemente un cliente, no el autor.

| Fecha | Hito |
|---|---|
| jul-2025 | El logo de la plataforma es una captura con esa fecha en el nombre del archivo |
| sep–nov 2025 | Primera infraestructura: `eargentyna[.]com` (panel «GreenProxy — Login») con subdominios que parecen códigos de país; se registra `greenproxysimpleserver[.]cc` |
| abr–nov 2026 | El panel «Green Proxy — Login» aparece en urlscan con el mismo HTML (SHA-256 `50448224…`) |
| ago-2026 | Despliegue en `yizhaojingyun[.]com`, un dominio reciclado, con más de 100 subdominios aleatorios |

**Para encontrar paneles nuevos:** en urlscan.io, busque `hash:50448224e0cb3dbcee198157ad6e01f3c59b36b7fb7e43601aa9f94ed842fb6a` (HTML del panel) o `hash:d1fc8bf9fbb5a0efaef075466ddb2531e07a7a6405e31d2155538c03af77f688` (logo).

**Relación con una botnet (campaña aparte en este repositorio):** el 6 de mayo de 2026, el mismo servidor que hoy hace de proxy (`94.26.106.29`, TechTies, AS197170) repartía binarios de **Mirai** desde `/bins/<arquitectura>`. URLhaus los registró y MalwareBazaar los clasifica como Mirai con la etiqueta «wraith», una variante sin reportes públicos. El servidor presentaba un certificado a nombre de `cnc.murrezbots[.]vip`, que todavía apunta a la misma IP. Los indicadores de la botnet van como campaña aparte, «Mirai «wraith» / murrezbots». Que sea el mismo operador que el phishing es **probable, no probado**: el proveedor pudo reasignar la IP.

## Qué hay aquí

| Ruta | Qué es | Para qué |
|---|---|---|
| [`IOCS.md`](IOCS.md) | Tabla legible por campaña, con los valores **desarmados** (`[.]`, `hxxps`), con rol, confianza y estado | Leer y citar en informes |
| [`feeds/`](feeds) | Un valor por línea, **sin desarmar**, de todas las campañas juntas | Cargar en el proxy, el DNS, el firewall o el SIEM |
| [`stix/`](stix) | Un paquete STIX 2.1 por campaña: la campaña, sus indicadores y las relaciones | MISP, OpenCTI, plataformas TAXII |
| [`yara/scgx02.yar`](yara/scgx02.yar) | Cinco reglas de SCGX02: el PDF señuelo, el gate de la landing, el loader cifrado, el panel y el JavaScript de la etapa 3 | Cazar en adjuntos, caché de proxy y kits recuperados |
| [`yara/rfq-aitm.yar`](yara/rfq-aitm.yar) | Tres reglas de la puerta RFQ: la primera visita (prueba de trabajo), la página con captcha y la trampa de herramientas de desarrollo | Cazar en capturas HTTP y caché de proxy |
| [`datos/iocs.csv`](datos/iocs.csv) | La fuente: todo lo demás se genera desde aquí. La columna `campana` dice a qué campaña pertenece cada IOC | Proponer cambios |

**Las reglas YARA** compilan con YARA 4.5. Se probaron contra las muestras del incidente: detectan el PDF señuelo, el gate de la landing y el loader cifrado. Contra 6.913 archivos limpios de un equipo de trabajo, 502 de ellos PDF, no dieron falsos positivos. La regla del JavaScript de la etapa 3 (v2) no tiene una muestra legible para probarla: el antivirus la bloquea. La regla del panel también salta con un documento que cite «SCGX02 PANEL»: úsela sobre capturas HTTP, no sobre informes.

**Las reglas de la puerta RFQ** se probaron contra las 26 respuestas que sirvió la infraestructura del actor el 3 de noviembre: detectan la primera visita, las seis páginas con captcha y todas las páginas del proxy, porque el kit inyecta la trampa de herramientas de desarrollo en cada página de Microsoft que reescribe. Contra 3.141 archivos limpios de un equipo de trabajo (2.553 JavaScript, 117 HTML, 216 JSON y 210 PDF, entre otros) no dieron falsos positivos.

**Cómo bloquear:** use `feeds/dominios.txt` **e incluya los subdominios** de los dominios base. Las landings usan subdominios nuevos con el nombre de cada víctima, que no se publican. `feeds/dominios_activos.txt` trae solo lo que seguía en pie en la última revalidación.

**Para encontrar paneles nuevos:** en urlscan.io, busque `hash:204a6074190b83402459e7402d13451443b72d4868eb4975d4dfffb420b4e57a`.

## Lo que este repositorio no publica, a propósito

- **Ningún dato de víctimas:** ni los subdominios de las landings (llevan el nombre de la empresa atacada), ni los remitentes, ni los asuntos o identificadores de los correos, ni los sitios legítimos comprometidos que el actor usó de paso. Para bloquear basta el dominio base. Un script rechaza cualquier valor que coincida con una lista local de términos que no se sube.
- **Direcciones IP de Cloudflare o de terceros:** las IP del borde de Cloudflare no se publican, porque bloquearlas cortaría sitios legítimos. Tampoco las IP residenciales usadas como proxy ni las de servidores de correo compartidos desde donde se enviaron los correos. Solo se publica la IP de **origen** de un servidor del actor cuando queda expuesta fuera de Cloudflare (`94.26.106.29` en la campaña RFQ): desde ahí el proxy inicia sesión en Microsoft, así que sirve para buscar en los registros de inicio de sesión.
- **Los buzones comprometidos y los sitios de paso** de la campaña RFQ: son empresas reales, víctimas también. Se publica el dominio que el actor registró para suplantar a una empresa, no la empresa suplantada.
- **Candidatos sin confirmar:** un dominio entra cuando sirve el kit, usa el panel o comparte su huella, no por parecido. Por eso `greenprox[.]cc` (mismo nombre de marca y mismo registrador, hoy suspendido) no está en los datos.

## Cómo se obtuvieron y cómo se revalidan

Para SCGX02 todo es **pasivo** y no se interactuó con la infraestructura del actor más allá de visitas públicas. Se usó DNS por DNS sobre HTTPS, Certificate Transparency y escaneos de urlscan.io (la visita la hace urlscan, solo con GET) sobre muestras del incidente. Nunca se enviaron credenciales ni POST a los paneles.

Para la campaña RFQ, además de lo anterior, se recorrió el enlace del incidente con un navegador controlado detrás de un proxy de interceptación, para ver lo que la puerta esconde de urlscan. Las reglas YARA y las rutas salen de esas respuestas.

Cada IOC lleva `estado` y `estado_al`: `activo`, `preparado` (página de prueba sin el kit), `bloqueado` (Cloudflare lo marca como phishing), `caido` o `sin_datos`. **Un dominio caído puede volver:** el actor reutiliza dominios base, así que se recomienda mantener el bloqueo.

## Mapeo a MITRE ATT&CK

| Técnica | Dónde |
|---|---|
| T1566.002 Phishing: enlace | PDF con enlace desde la cuenta de un proveedor |
| T1199 Relación de confianza | El proveedor comprometido como remitente |
| T1557 Adversario en el medio | Proxy en tiempo real de usuario, contraseña y segundo factor |
| T1539 Robo de la cookie de sesión | La sesión robada se usa después del segundo factor |
| T1583.001 Adquirir infraestructura: dominios | Dominios base `.de` registrados en tandas |
| T1583.006 Adquirir infraestructura: servicios web | Buckets de Tencent Cloud, AWS S3, Linode y Azure Blob |
| T1564.008 Ocultar artefactos: reglas de correo | Reglas de bandeja que mueven y marcan avisos como leídos |
| T1586.002 Comprometer cuentas: correo | RFQ: el primer contacto sale de buzones reales comprometidos |
| T1656 Suplantación | RFQ: dominio registrado para hacerse pasar por una empresa real |
| T1497 Evasión de entornos virtuales y de análisis | RFQ: `/.verify`, `/.detect` y `/.devtools` mandan a los analistas a otro sitio |

## Contribuir

Para un IOC nuevo o una corrección (por ejemplo, un dominio que cambió de dueño), abra un *issue* o un *pull request* que modifique solo `datos/iocs.csv`, y luego corra:

```bash
python scripts/construir.py
python -m unittest discover -s tests
```

La integración continua comprueba que los archivos generados coincidan con el CSV. **No incluya datos de víctimas.** Si cree que un IOC es un falso positivo, abra un *issue*: se revisa y, si corresponde, se marca o se retira.

## Licencia y aviso

Datos y reglas bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es) (cite «Raiku Solutions, IOC de SCGX02 / CodeStorm» o «Raiku Solutions, IOC de la campaña RFQ en dos pasos»). El script bajo licencia MIT. Se entrega **sin garantía:** pruebe antes de bloquear en producción.

---

## English summary

**Write-up:** [Green Proxy: a first look at an undocumented AiTM phishing-as-a-service platform](https://raiku.cl/research/green-proxy).

IOCs for two adversary-in-the-middle (AiTM) phishing campaigns against Microsoft 365:

- **SCGX02 / CodeStorm**, delivered from compromised supplier mailboxes. The kit uses Cloudflare-fronted `.de` domains, an operator panel branded "SCGX02 PANEL" with a constant HTML hash (`204a6074…`), and the phishing UI hosted on Tencent Cloud COS buckets.
- **Two-step RFQ / AiTM proxy**: a link-free request for quotation from a compromised mailbox, then a follow-up from a lookalike domain whose link abuses an open OAuth redirect. It ends at a phishing-as-a-service gate on `yizhaojingyun[.]com` (proof of work, browser fingerprint, sandbox and devtools detection, own captcha on `greenproxysimpleserver[.]cc`) in front of a real-time Microsoft sign-in proxy.

- `IOCS.md`: defanged, human-readable table with role, confidence and last-known status.
- `feeds/`: raw one-per-line lists. Block the base domains **including all subdomains**: per-victim landing subdomains are intentionally not published.
- `feeds/` covers both campaigns; `IOCS.md` and `stix/` are split per campaign (`datos/iocs.csv`, column `campana`).
- `stix/scgx02.json`, `stix/rfq-aitm.json`: STIX 2.1 bundles (campaign, indicators, relationships). Marked TLP:WHITE in STIX, which is TLP:CLEAR.
- `yara/scgx02.yar` (five rules) and `yara/rfq-aitm.yar` (three rules for the RFQ gate).

Collection was passive only (DoH, Certificate Transparency, urlscan.io). No victim data, no Cloudflare edge IPs and no unconfirmed lookalikes are published. Licensed CC BY 4.0 (data and rules) and MIT (script).
