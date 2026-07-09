def montar_html_prospeccao(texto_ia):
    paragrafos_html = ""
    linhas = texto_ia.strip().split("\n\n")
    for linha in linhas:
        if linha.strip():
            if "atenciosamente" in linha.lower():
                paragrafos_html += f'<p style="margin:0 0 20px 0; color:#0b3d91; font-size:16px; line-height:1.8; font-weight:bold;">{linha.strip()}</p>'
            else:
                paragrafos_html += f'<p style="margin:0 0 20px 0; color:#334155; font-size:16px; line-height:1.8;">{linha.strip()}</p>'

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conceito Cargas Aéreas</title>
    </head>
    <body style="margin:0; padding:0; background:#eef2f7; font-family:Arial, Helvetica, sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center" style="padding:40px 15px;">

                <table width="620" cellpadding="0" cellspacing="0" border="0" style="
                    background:#ffffff;
                    border-radius:12px;
                    overflow:hidden;
                    box-shadow:0 4px 20px rgba(0,0,0,0.05);
                ">

                    <tr>
                        <td style="
                            background:linear-gradient(135deg, #071a35 0%, #0b3d91 100%);
                            padding:25px 40px;
                            text-align:left;
                        ">
                            <img src="cid:logo" width="160" alt="CONCEITO CARGAS AÉREAS" style="display:block;">
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:45px 40px 30px 40px;">
                            
                            {paragrafos_html}
                            
                            <img src="cid:assinatura" width="200" alt="Assinatura" style="display:block; margin:20px auto;">

                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8fafc; border-radius:14px; border:1px solid #e2e8f0; margin:25px 0 0 0;">
                                <tr>
                                    <td style="padding:20px 25px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td width="50%" style="vertical-align:top; padding:0 10px 0 0;">
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                        <tr>
                                                            <td style="padding-bottom:6px;">
                                                                <strong style="color:#0b3d91; font-size:14px;">Matriz Fortaleza</strong>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td>
                                                                <a href="https://wa.me/558592571233" target="_blank" style="display:inline-block; background:#25D366; color:#ffffff; text-decoration:none; padding:7px 16px; border-radius:20px; font-size:12px; font-weight:bold; letter-spacing:0.3px;">Conversar agora</a>
                                                                <span style="color:#64748b; font-size:13px; margin-left:8px;">85 9257-1233</span>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                                <td width="50%" style="vertical-align:top; padding:0 0 0 10px;">
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                        <tr>
                                                            <td style="padding-bottom:6px;">
                                                                <strong style="color:#0b3d91; font-size:14px;">Filial São Paulo</strong>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td>
                                                                <a href="https://wa.me/5511975001368" target="_blank" style="display:inline-block; background:#25D366; color:#ffffff; text-decoration:none; padding:7px 16px; border-radius:20px; font-size:12px; font-weight:bold; letter-spacing:0.3px;">Conversar agora</a>
                                                                <span style="color:#64748b; font-size:13px; margin-left:8px;">11 97500-1368</span>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <hr style="border:none; border-top:1px solid #e2e8f0; margin:35px 0 25px 0;">
                            
                            <p style="margin:0; color:#64748b; font-size:14px; line-height:1.6;">
                                <strong>Precisa de agilidade logística agora?</strong><br>
                                Responda este email ou acesse nossos <a href="https://www.conceitocargasaereas.com.br/contato" style="color:#0b3d91; text-decoration:none; font-weight:bold;">Canais De Atendimento</a>.
                            </p>

                            <hr style="border:none; border-top:1px solid #e2e8f0; margin:40px 0 30px 0;">

                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td align="center" style="padding:0 8px;">
                                        <img src="https://www.conceitocargasaereas.com.br/logos/Brudam.svg" width="85" alt="Brudam" style="display:block; opacity:0.85;">
                                    </td>
                                    <td align="center" style="padding:0 8px;">
                                        <img src="https://www.conceitocargasaereas.com.br/logos/antt.png" width="82" alt="ANTT" style="display:block; opacity:0.85;">
                                    </td>
                                    <td align="center" style="padding:0 8px;">
                                        <img src="https://www.conceitocargasaereas.com.br/logos/anvisa.png" width="70" alt="ANVISA" style="display:block; opacity:0.85;">
                                    </td>
                                    <td align="center" style="padding:0 8px;">
                                        <img src="https://www.conceitocargasaereas.com.br/logos/sompo.svg" width="95" alt="SOMPO" style="display:block; opacity:0.85;">
                                    </td>
                                    <td align="center" style="padding:0 8px;">
                                        <img src="https://www.conceitocargasaereas.com.br/logos/autotrac.svg" width="98" alt="AUTOTRAC" style="display:block; opacity:0.85;">
                                    </td>
                                    <td align="center" style="padding:0 8px;">
                                        <img src="https://www.conceitocargasaereas.com.br/logos/servis.png" width="74" alt="SERVIS" style="display:block; opacity:0.85;">
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <tr>
                        <td style="
                            background:#f8fafc;
                            padding:20px 40px;
                            text-align:center;
                            border-top:1px solid #e2e8f0;
                        ">
                            <p style="margin:0; color:#94a3b8; font-size:12px;">
                                © 2026 <a href="https://www.conceitocargasaereas.com.br" style="color:#0b3d91; text-decoration:none; font-weight:bold;">CONCEITO CARGAS AÉREAS</a>. Todos os direitos reservados.
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
    </body>
    </html>
    """
    return html
