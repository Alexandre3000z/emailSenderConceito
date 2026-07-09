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
CHECKPOINT_FILE = os.getenv("CHECKPOINT_FILE", "checkpoint.json")
LIMITE_DIARIO = int(os.getenv("LIMITE_DIARIO", "75"))
INTERVALO_MIN = int(os.getenv("INTERVALO_MIN", "90"))
INTERVALO_MAX = int(os.getenv("INTERVALO_MAX", "180"))
