/*
   Campaña «RFQ en dos pasos / proxy AiTM» — Raiku Solutions, TLP:CLEAR, CC BY 4.0.
   Reglas para la puerta anti-análisis que protege el proxy AiTM. Probadas contra las páginas que sirvió la puerta
   el 2026-11-03 (primera visita, página con captcha y páginas del proxy). Úselas sobre capturas HTTP o caché de proxy.
*/

rule PHISH_Kit_RFQ_AiTM_Gate_ProofOfWork
{
    meta:
        description = "Primera visita a la puerta: prueba de trabajo, huella del navegador y POST a /.verify, que entrega la cookie _vfy"
        author = "Raiku Solutions"
        date = "2026-11-03"
        tlp = "CLEAR"
    strings:
        $verify = "+\"/.verify\"" ascii
        $detect = "fetch(\"/.detect\"" ascii
        $sig = "sig_score:sig,sig_flags:flags" ascii
        $cookie = "document.cookie=\"_vfy=\"" ascii
        $render = "rs.push(\"sw_renderer\")" ascii
    condition:
        filesize < 300KB and 4 of them
}

rule PHISH_Kit_RFQ_AiTM_Gate_Captcha
{
    meta:
        description = "Segunda visita a la puerta: «Security Check» con captcha propio de prueba de trabajo y detector de entornos de análisis"
        author = "Raiku Solutions"
        date = "2026-11-03"
        tlp = "CLEAR"
    strings:
        $flag = "const USE_HCAPTCHA" ascii
        $sitekey = "24600978-7df2-44bc-9a8c-a18c95ca6886" ascii
        $verify = "/captcha/verify`" ascii
        $sandbox = "type:\"sandbox\"" ascii
        $ent = "ent_count:0" ascii
    condition:
        filesize < 300KB and 4 of them
}

rule PHISH_Kit_RFQ_AiTM_DevTools_Trap
{
    meta:
        description = "Trampa de herramientas de desarrollo que el kit inyecta en la puerta y en cada página de Microsoft que reescribe el proxy: avisa con POST a /.devtools y saca al analista"
        author = "Raiku Solutions"
        date = "2026-11-03"
        tlp = "CLEAR"
    strings:
        $report = "function reportDT(" ascii
        $post = "fetch(\"/.devtools\"" ascii
    condition:
        filesize < 300KB and all of them
}
