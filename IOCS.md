# IOC publicados por Raiku Solutions (versión 2026-11-03)

Tabla generada desde `datos/iocs.csv` con `scripts/construir.py`. Los valores están desarmados (`[.]`, `hxxps`) para que no se puedan abrir por error.
Los valores tal cual, para cargar en un bloqueo, están en `feeds/` (todas las campañas juntas), y un paquete STIX 2.1 por campaña en `stix/`.

## SCGX02 / CodeStorm (versión 2026-11-01, `stix/scgx02.json`)

### Dominios base (20)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `chairoftime[.]de` | dominio base del kit | alta | 2026-10-19 | activo (2026-11-01) | panel tundra30 |
| `essentialdocstorage[.]de` | dominio base del kit | alta | 2026-10-22 | activo (2026-11-01) | panel pierce99 |
| `forestgolem[.]de` | dominio base del kit | alta | 2026-10-22 | activo (2026-11-01) | panel pierce16 |
| `gentlesunrise[.]de` | dominio base del kit | alta | 2026-10-16 | activo (2026-11-01) | aloja el panel beta y una landing tras Turnstile |
| `goldenvisionsforest[.]de` | dominio base del kit | alta | 2026-10-22 | activo (2026-11-01) | panel granite10 |
| `hcenginreering[.]net` | dominio base de landings | alta | 2026-10-30 | activo (2026-11-01) | sus landings llaman al panel quill99 |
| `morningbreezeflowers[.]de` | dominio base del kit | alta | 2026-10-22 | activo (2026-11-01) | panel vault53 |
| `preparednessmatters[.]de` | dominio base del kit | alta | 2026-10-16 | activo (2026-11-01) | panel pierce35 |
| `shimmeringglow[.]de` | dominio base del kit | alta | 2026-10-07 | activo (2026-11-01) | panel quill99 |
| `silverstreetmoon[.]de` | dominio base del kit | alta | 2026-10-16 | activo (2026-11-01) | panel zephyr71 |
| `sleepingforestmystery[.]de` | dominio base del kit | alta | 2026-10-22 | activo (2026-11-01) | panel jasper67 |
| `whispersofgoldenlight[.]de` | dominio base del kit | alta | 2026-10-16 | activo (2026-11-01) | panel cedar69 |
| `ancientrooftops[.]de` | dominio base del kit (señuelos en sueco) | alta | 2026-10-19 | bloqueado (2026-11-01) | panel lunar64 bloqueado por Cloudflare |
| `comrandjet[.]com` | dominio base de landings | alta | 2026-10-14 | sin datos (2026-11-01) | usaba el panel quill99 |
| `eagerlyshowingoff[.]de` | dominio base preparado | media | 2026-10-20 | sin datos (2026-11-01) | página de prueba de AlmaLinux |
| `harmonyofnature[.]de` | dominio base del kit (versión 1; agosto de 2026) | alta | 2026-10-18 | bloqueado (2026-11-01) | Cloudflare lo marca como phishing |
| `morningmystery[.]de` | dominio base del kit | alta | 2026-10-16 | caido (2026-11-01) | panel quartz84 |
| `seatofpresence[.]de` | dominio base del kit (campaña de octubre) | alta | 2026-10-07 | caido (2026-11-01) | dominio estacionado; el panel raven81 cayó |
| `sleepingforestmagic[.]de` | dominio base preparado | media | 2026-10-20 | preparado (2026-11-01) | página de prueba de AlmaLinux |
| `softlycloaked[.]de` | dominio base del kit (septiembre de 2026) | alta | 2026-10-18 | caido (2026-11-01) |  |

### Hosts (37)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `beta[.]gentlesunrise[.]de` | panel del operador | alta | 2026-10-16 | activo (2026-11-01) | mismo HTML de panel; desde el 1-nov la raíz es una landing tras Turnstile |
| `cedar69[.]whispersofgoldenlight[.]de` | panel del operador | alta | 2026-10-16 | activo (2026-11-01) | mismo HTML de panel |
| `granite10[.]goldenvisionsforest[.]de` | panel del operador | alta | 2026-10-22 | activo (2026-11-01) | mismo HTML de panel |
| `jasper67[.]sleepingforestmystery[.]de` | panel del operador | alta | 2026-10-22 | activo (2026-11-01) | mismo HTML de panel |
| `pierce16[.]forestgolem[.]de` | panel del operador | alta | 2026-10-22 | activo (2026-11-01) | mismo HTML de panel |
| `pierce35[.]preparednessmatters[.]de` | panel del operador | alta | 2026-10-16 | activo (2026-11-01) | mismo HTML de panel |
| `pierce99[.]essentialdocstorage[.]de` | panel del operador | alta | 2026-10-22 | activo (2026-11-01) | mismo HTML de panel |
| `quill99[.]shimmeringglow[.]de` | panel del operador | alta | 2026-10-16 | activo (2026-11-01) | mismo HTML de panel (204a6074…) |
| `tundra30[.]chairoftime[.]de` | panel del operador | alta | 2026-10-19 | activo (2026-11-01) | mismo HTML de panel |
| `vault53[.]morningbreezeflowers[.]de` | panel del operador | alta | 2026-10-22 | activo (2026-11-01) | mismo HTML de panel |
| `zephyr71[.]silverstreetmoon[.]de` | panel del operador | alta | 2026-10-16 | activo (2026-11-01) | mismo HTML de panel |
| `alladokument[.]ancientrooftops[.]de` | landing (señuelo en sueco) | alta | 2026-10-19 | sin datos (2026-11-01) |  |
| `cdstyr546tt54re5ty6y5-1457164341[.]cos[.]na-siliconvalley[.]myqcloud[.]com` | bucket de Tencent COS (versión 1) | alta | 2026-10-18 | sin datos (2026-11-01) |  |
| `enrollments[.]sleepingforestmagic[.]de` | host preparado | media | 2026-10-26 | preparado (2026-11-01) | página de prueba de AlmaLinux |
| `fileviewall[.]ancientrooftops[.]de` | landing | alta | 2026-10-26 | bloqueado (2026-11-01) |  |
| `hfkme[.]blob[.]core[.]windows[.]net` | salto de redirección (Azure Blob) | alta | 2026-10-18 | sin datos (2026-11-01) |  |
| `hjzok[.]harmonyofnature[.]de` | panel del kit (versión 1) | alta | 2026-10-18 | bloqueado (2026-11-01) | /capt.php |
| `htgftyhy6565tt54rr43-1457164341[.]cos[.]na-siliconvalley[.]myqcloud[.]com` | bucket de Tencent COS | alta | 2026-10-18 | sin datos (2026-11-01) |  |
| `keluar[.]forestgolem[.]de` | host preparado | media | 2026-10-29 | preparado (2026-11-01) | página de prueba de AlmaLinux |
| `krypton85-6f10-1483637648[.]cos[.]na-siliconvalley[.]myqcloud[.]com` | bucket de Tencent COS | alta | 2026-10-18 | sin datos (2026-11-01) |  |
| `lunar64-9eb9-1483637648[.]cos[.]na-siliconvalley[.]myqcloud[.]com` | bucket de Tencent COS | alta | 2026-10-22 | sin datos (2026-11-01) |  |
| `lunar64[.]ancientrooftops[.]de` | panel del operador | alta | 2026-10-19 | bloqueado (2026-11-01) |  |
| `msoff-standard-cran-v557br-com[.]id-cgk-1[.]linodeobjects[.]com` | página de phishing (Linode Object Storage) | alta | 2026-10-16 | sin datos (2026-11-01) |  |
| `onffline0901[.]survey-terminaloffviceadmimsurrond[.]cloud` | salto de entrega (señuelo «Adobe Acrobat») | media | 2026-10-13 | sin datos (2026-11-01) |  |
| `pierce99-e28e-1483637648[.]cos[.]na-siliconvalley[.]myqcloud[.]com` | bucket de Tencent COS | alta | 2026-10-22 | sin datos (2026-11-01) |  |
| `public-resource-4896531063069088[.]s3[.]ap-south-1[.]amazonaws[.]com` | salto de redirección (AWS S3) | alta | 2026-10-16 | sin datos (2026-11-01) |  |
| `puvzivjkgpjaqnpjlkyb[.]softlycloaked[.]de` | landing | alta | 2026-10-18 | caido (2026-11-01) |  |
| `quartz84-bd54-1497982805[.]cos[.]na-siliconvalley[.]myqcloud[.]com` | bucket de Tencent COS (etapa 3) | alta | 2026-10-16 | sin datos (2026-11-01) |  |
| `quartz84[.]morningmystery[.]de` | panel del operador | alta | 2026-10-16 | caido (2026-11-01) |  |
| `quill99-55d7-1497982805[.]cos[.]na-siliconvalley[.]myqcloud[.]com` | bucket de Tencent COS (etapa 3) | alta | 2026-10-16 | sin datos (2026-11-01) |  |
| `raven81-32b7-1497982805[.]cos[.]na-siliconvalley[.]myqcloud[.]com` | bucket de Tencent COS con la interfaz de phishing (etapa 3) | alta | 2026-10-16 | sin datos (2026-11-01) |  |
| `raven81[.]seatofpresence[.]de` | panel del operador y robo de credenciales | alta | 2026-10-16 | caido (2026-11-01) | /panel/ y /google.php |
| `sakrafiler[.]ancientrooftops[.]de` | landing (señuelo en sueco) | alta | 2026-10-19 | sin datos (2026-11-01) |  |
| `vault53-d309-1497982805[.]cos[.]na-siliconvalley[.]myqcloud[.]com` | bucket de Tencent COS (etapa 3) | alta | 2026-10-22 | sin datos (2026-11-01) |  |
| `viewdocu[.]ancientrooftops[.]de` | landing | alta | 2026-10-19 | sin datos (2026-11-01) |  |
| `zephyr71-4bd9-1483637648[.]cos[.]na-siliconvalley[.]myqcloud[.]com` | bucket de Tencent COS | alta | 2026-10-18 | caido (2026-11-01) | dado de baja por Tencent |
| `zgpvvyxjngmpbowhwdtm[.]morningmystery[.]de` | landing | alta | 2026-10-16 | caido (2026-11-01) |  |

### URLs (6)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `hxxps://quill99[.]shimmeringglow[.]de/panel/?api&visit` | contador de visitas del panel | alta | 2026-10-30 | activo (2026-11-01) | lo llaman las landings de hcenginreering.net |
| `hxxps://flyn[.]co/pKaYZP` | acortador hacia landings de lunar64 | media | 2026-10-12 | sin datos (2026-11-01) |  |
| `hxxps://hfkme[.]blob[.]core[.]windows[.]net/hfkme/hfk.html` | salto de redirección | alta | 2026-10-18 | sin datos (2026-11-01) |  |
| `hxxps://hjzok[.]harmonyofnature[.]de/capt.php` | robo de credenciales (versión 1) | alta | 2026-10-18 | bloqueado (2026-11-01) |  |
| `hxxps://raven81[.]seatofpresence[.]de/google.php` | robo de credenciales en tiempo real | alta | 2026-10-16 | caido (2026-11-01) |  |
| `hxxps://raven81[.]seatofpresence[.]de/panel/?api&visit` | contador de visitas del panel | alta | 2026-10-16 | caido (2026-11-01) |  |

### Archivos (SHA-256) (4)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `17299201e289b01ae7ba077ba9a56a4a8f810613c9f6476fe16df945906d899a` | JavaScript del kit (etapa 3; versión 1) | alta | 2026-10-18 | — |  |
| `204a6074190b83402459e7402d13451443b72d4868eb4975d4dfffb420b4e57a` | HTML del panel /panel/ («SCGX02 PANEL») | alta | 2026-10-19 | — | buscar en urlscan con hash:<valor> para encontrar paneles |
| `965491e2aa913bcee12580f20f16f3f70d9c26b3b31cb7ade46a742758e8903a` | PDF señuelo cifrado | alta | 2026-10-16 | — | una página con una imagen y un enlace oculto |
| `aa7351b192f1e577e2033e114155d9ce520762e1abd19a4b3b777b4483ffbb4c` | JavaScript del kit (etapa 3; versión 2) | alta | 2026-10-18 | — |  |

### Archivos (MD5) (1)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `c09b8641a009226432dc9a00d75a09d6` | PDF señuelo cifrado | alta | 2026-10-16 | — |  |

### Certificados (SHA-256) (4)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `055808552ea0e0303ea1e9847646df891f073a194f9c7e249b7067c1e7be6242` | certificado comodín Sectigo *.softlycloaked.de | media | 2026-10-18 | — |  |
| `26496f25f0062e7cf05b833dcdac92192114ad4403dc746794348af9c17eac35` | certificado comodín Sectigo *.chairoftime.de | media | 2026-10-19 | — |  |
| `a75f412779e733cd66987f482688a36bf354fa590746614f0ddbc430095db944` | certificado comodín Sectigo *.softlycloaked.de | media | 2026-10-18 | — |  |
| `d19763e2452f2f684756a182bf26b5e2bde07879fecc3f8c2cfc10ade4c1532b` | certificado comodín Sectigo *.seatofpresence.de | media | 2026-10-16 | — | probablemente en el origen |

### Cadenas para cazar (6)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `1457164341` | APPID de Tencent Cloud de los buckets (versión 1) | alta | 2026-10-18 | — |  |
| `1483637648` | APPID de Tencent Cloud de los buckets | alta | 2026-10-18 | — |  |
| `1497982805` | APPID de Tencent Cloud de los buckets | alta | 2026-10-16 | — |  |
| `SCGX02 PANEL` | marca del panel del operador | alta | 2026-10-16 | — |  |
| `e20e2de7dca648d8846620b76a7849c5` | token de Cloudflare Web Analytics compartido por landings y panel | alta | 2026-10-16 | — |  |
| `wfrsx_0x3197` | identificador del ofuscador del kit (versión 2) | alta | 2026-10-18 | — |  |

## RFQ en dos pasos / proxy AiTM (versión 2026-11-03, `stix/rfq-aitm.json`)

### Dominios base (3)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `greenproxysimpleserver[.]cc` | captcha propio del kit | alta | 2026-11-03 | activo (2026-11-03) | servicio en el puerto 8443 detrás de Cloudflare: /captcha/api y /captcha/verify (prueba de trabajo SHA-256) |
| `ipfs-us[.]com` | dominio que suplanta a una empresa estadounidense de financiamiento de primas | alta | 2026-11-03 | activo (2026-11-03) | registrado el 2026-05-18 (NameSilo); correo en Google Workspace con DKIM propio y sin DMARC; envía la continuación con el enlace |
| `yizhaojingyun[.]com` | dominio base de la puerta y del proxy AiTM | alta | 2026-11-03 | activo (2026-11-03) | registrado el 2026-08-24 (NiceNIC); DNS en Cloudflare pero con el registro A apuntando al origen; certificado desde el 2026-09-07; atiende a varias campañas |

### Hosts (5)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `a4vhglh3m[.]yizhaojingyun[.]com` | puerta anti-análisis (sistema de distribución de tráfico) | alta | 2026-11-03 | activo (2026-11-03) | /.verify, /.detect y /.devtools; los bots terminan en stackoverflow.com o google.com |
| `loginlive[.]yizhaojingyun[.]com` | reflejo de login.live.com | alta | 2026-11-03 | activo (2026-11-03) | sirve /Me.htm |
| `loginms[.]yizhaojingyun[.]com` | reflejo de login.microsoft.com | alta | 2026-11-03 | activo (2026-11-03) | sirve /.well-known/webauthn con los orígenes del proxy |
| `tfgevds[.]yizhaojingyun[.]com` | proxy AiTM del inicio de sesión de Microsoft | alta | 2026-11-03 | activo (2026-11-03) | reenvía usuario, contraseña y cookies de sesión a Entra ID en tiempo real |
| `www[.]yizhaojingyun[.]com` | salto con token de un solo uso hacia el proxy | alta | 2026-11-03 | activo (2026-11-03) | rutas /p/<token> |

### URLs (1)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `hxxps://a4vhglh3m[.]yizhaojingyun[.]com/v1df2lmz-gpl5fqfab2-vpd6dfbxiwgsg-8iyxionbd8wsj` | entrada de la puerta usada en la campaña | alta | 2026-11-03 | activo (2026-11-03) | genérica, sin el correo de la víctima; el kit acepta el correo en #correo, ?email= o ?e= |

### Direcciones IP (1)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `94[.]26[.]106[.]29` | origen de yizhaojingyun.com (fuera de Cloudflare) | alta | 2026-11-03 | activo (2026-11-03) | hosting Techties (Bulgaria) con IP alemana; desde aquí el proxy inicia sesión en Microsoft: buscarla en los inicios de sesión de Entra ID |

### Cadenas para cazar (6)

| Valor | Rol | Confianza | Visto por primera vez | Estado | Notas |
|---|---|---|---|---|---|
| `/.detect` | ruta POST del detector de entornos de análisis | alta | 2026-11-03 | — | cuerpo JSON con type "sandbox", score, rs, url y ent_count |
| `/.devtools` | ruta POST que avisa si se abren las herramientas de desarrollo | alta | 2026-11-03 | — | oculta la página y redirige a google.com |
| `/.verify` | ruta POST de la puerta: prueba de trabajo y huella del navegador | alta | 2026-11-03 | — | cuerpo JSON con challenge_id, solution, sig_score, sig_flags, fp, tz, tz_off, hc y dm |
| `24600978-7df2-44bc-9a8c-a18c95ca6886` | sitekey de hCaptcha configurada en el kit | media | 2026-11-03 | — | hCaptcha venía apagado (USE_HCAPTCHA = false); sirve para relacionar otras campañas del mismo kit |
| `_vfy` | cookie de la puerta | media | 2026-11-03 | — | válida 7 días en el dominio base |
| `prompt=none&id_token_hint=dummy` | abuso de redirección OAuth abierta en el enlace del correo | media | 2026-11-03 | — | un endpoint /oauth/authorize legítimo devuelve error y redirige igual al redirect_uri del actor |
