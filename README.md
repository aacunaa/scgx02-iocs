# IOC de SCGX02 / CodeStorm

Indicadores de compromiso de una campaña de **phishing de adversario en el medio (AiTM)** contra cuentas de Microsoft 365. Los publica **Raiku Solutions** a partir de una investigación de respuesta a incidentes en Chile (octubre y noviembre de 2026). **TLP:CLEAR:** se pueden compartir sin restricción.

*English summary below.*

## La campaña en cinco líneas

1. **Entrega:** el correo llega desde la cuenta real de un proveedor comprometido, así que pasa SPF, DKIM y DMARC. El señuelo es una invitación a licitar con un PDF cifrado de una página: una imagen y un enlace oculto.
2. **Landing:** el enlace lleva a un subdominio con el nombre de la víctima, bajo un dominio base del actor detrás de Cloudflare. Hay un control anti-bots propio («Secure Access Check») o Turnstile.
3. **Robo:** la interfaz de phishing (etapa 3) se carga desde buckets de Tencent Cloud y reenvía usuario, contraseña y segundo factor en tiempo real al panel del operador.
4. **Panel:** el panel «SCGX02 PANEL» se publica en `/panel/` de un host con nombre corto y número (`pierce16`, `quill99`, `vault53`…). Todos sirven el mismo HTML: SHA-256 `204a6074…`.
5. **Después:** inicios de sesión desde la infraestructura del kit y reglas de bandeja que esconden avisos.

## Qué hay aquí

| Ruta | Qué es | Para qué |
|---|---|---|
| [`IOCS.md`](IOCS.md) | Tabla legible con los valores **desarmados** (`[.]`, `hxxps`), con rol, confianza y estado | Leer y citar en informes |
| [`feeds/`](feeds) | Un valor por línea, **sin desarmar** | Cargar en el proxy, el DNS, el firewall o el SIEM |
| [`stix/scgx02.json`](stix/scgx02.json) | Paquete STIX 2.1: una campaña, sus indicadores y las relaciones | MISP, OpenCTI, plataformas TAXII |
| [`yara/scgx02.yar`](yara/scgx02.yar) | Cinco reglas: el PDF señuelo, el gate de la landing, el loader cifrado, el panel y el JavaScript de la etapa 3 | Cazar en adjuntos, caché de proxy y kits recuperados |
| [`datos/iocs.csv`](datos/iocs.csv) | La fuente: todo lo demás se genera desde aquí | Proponer cambios |

**Cómo bloquear:** use `feeds/dominios.txt` **e incluya los subdominios** de los dominios base. Las landings usan subdominios nuevos con el nombre de cada víctima, que no se publican. `feeds/dominios_activos.txt` trae solo lo que seguía en pie en la última revalidación.

**Para encontrar paneles nuevos:** en urlscan.io, busque `hash:204a6074190b83402459e7402d13451443b72d4868eb4975d4dfffb420b4e57a`.

## Lo que este repositorio no publica, a propósito

- **Ningún dato de víctimas:** ni los subdominios de las landings (llevan el nombre de la empresa atacada), ni los remitentes, ni los asuntos o identificadores de los correos, ni los sitios legítimos comprometidos que el actor usó de paso. Para bloquear basta el dominio base. Un script rechaza cualquier valor que coincida con una lista local de términos que no se sube.
- **Direcciones IP:** el actor publica todo detrás de Cloudflare, así que las IP que se ven son del borde de Cloudflare y bloquearlas cortaría sitios legítimos. Tampoco se publican IP residenciales usadas como proxy, porque pueden ser de personas sin relación con el ataque.
- **Candidatos sin confirmar:** un dominio entra cuando sirve el kit, usa el panel o comparte su huella, no por parecido.

## Cómo se obtuvieron y cómo se revalidan

Todo es **pasivo** y no se interactuó con la infraestructura del actor más allá de visitas públicas. Se usó DNS por DNS sobre HTTPS, Certificate Transparency y escaneos de urlscan.io (la visita la hace urlscan, solo con GET) sobre muestras del incidente. Nunca se enviaron credenciales ni POST a los paneles.

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

## Contribuir

Para un IOC nuevo o una corrección (por ejemplo, un dominio que cambió de dueño), abra un *issue* o un *pull request* que modifique solo `datos/iocs.csv`, y luego corra:

```bash
python scripts/construir.py
python -m unittest discover -s tests
```

La integración continua comprueba que los archivos generados coincidan con el CSV. **No incluya datos de víctimas.** Si cree que un IOC es un falso positivo, abra un *issue*: se revisa y, si corresponde, se marca o se retira.

## Licencia y aviso

Datos y reglas bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es) (cite «Raiku Solutions, IOC de SCGX02 / CodeStorm»). El script bajo licencia MIT. Se entrega **sin garantía:** pruebe antes de bloquear en producción.

---

## English summary

IOCs for **SCGX02 / CodeStorm**, an adversary-in-the-middle (AiTM) phishing campaign against Microsoft 365, delivered from compromised supplier mailboxes. The kit uses Cloudflare-fronted `.de` domains, an operator panel branded "SCGX02 PANEL" with a constant HTML hash (`204a6074…`), and the phishing UI hosted on Tencent Cloud COS buckets.

- `IOCS.md`: defanged, human-readable table with role, confidence and last-known status.
- `feeds/`: raw one-per-line lists. Block the base domains **including all subdomains**: per-victim landing subdomains are intentionally not published.
- `stix/scgx02.json`: STIX 2.1 bundle (campaign, indicators, relationships). Marked TLP:WHITE in STIX, which is TLP:CLEAR.
- `yara/scgx02.yar`: five hunting rules.

Collection was passive only (DoH, Certificate Transparency, urlscan.io). No victim data, no Cloudflare edge IPs and no unconfirmed lookalikes are published. Licensed CC BY 4.0 (data and rules) and MIT (script).
