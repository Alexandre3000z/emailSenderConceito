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
                            
                            <img src="cid:assinatura" width="200" alt="Assinatura" style="display:block; margin:20px 0;">
                            
                            <hr style="border:none; border-top:1px solid #e2e8f0; margin:35px 0 25px 0;">
                            
                            <p style="margin:0; color:#64748b; font-size:14px; line-height:1.6;">
                                <strong>Precisa de agilidade logística agora?</strong><br>
                                Responda este email ou acesse nossos <a href="https://www.conceitocargasaereas.com.br/contato" style="color:#0b3d91; text-decoration:none; font-weight:bold;">Canais De Atendimento</a>.
                            </p>
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
