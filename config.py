import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_EMAIL = os.getenv("SENHA_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.hostinger.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
ARQUIVO_ENTRADA = os.getenv("ARQUIVO_ENTRADA")
ARQUIVO_SAIDA = os.getenv("ARQUIVO_SAIDA", "resultado_campanha.xlsx")
