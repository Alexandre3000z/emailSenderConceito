import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from config import EMAIL_REMETENTE, SENHA_EMAIL, SMTP_SERVER, SMTP_PORT
from email_builder import montar_html_prospeccao


def enviar_email(destinatario, assunto, texto_ia):
    corpo_html = montar_html_prospeccao(texto_ia)

    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario
    msg["Subject"] = assunto

    with open("Branco (1).png", "rb") as f:
        logo = MIMEImage(f.read(), name="logo.png")
        logo.add_header("Content-ID", "<logo>")
        logo.add_header("Content-Disposition", "inline", filename="logo.png")
        msg.attach(logo)

    with open("assinatura.png", "rb") as f:
        assinatura = MIMEImage(f.read(), name="assinatura.png")
        assinatura.add_header("Content-ID", "<assinatura>")
        assinatura.add_header("Content-Disposition", "inline", filename="assinatura.png")
        msg.attach(assinatura)

    msg.attach(MIMEText(texto_ia, "plain", "utf-8"))
    msg.attach(MIMEText(corpo_html, "html", "utf-8"))

    try:
        servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
        servidor.send_message(msg)
        print("   ✅ Email enviado com sucesso no Hostinger!")
        servidor.quit()
        return True
    except Exception as e:
        print(f"   ❌ Erro ao enviar pelo Hostinger: {e}")
        return False
