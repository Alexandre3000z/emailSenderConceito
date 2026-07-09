import json
import time
import ast
import random
from datetime import datetime
from pathlib import Path

import pandas as pd

from config import (
    ARQUIVO_ENTRADA,
    ARQUIVO_SAIDA,
    CHECKPOINT_FILE,
    LIMITE_DIARIO,
    INTERVALO_MIN,
    INTERVALO_MAX,
)
from ai_client import gerar_email_ia
from smtp_client import enviar_email


def carregar_checkpoint():
    caminho = Path(CHECKPOINT_FILE)
    if caminho.exists():
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "ultima_data": "",
        "enviados_hoje": 0,
        "total_enviados": 0,
        "emails_enviados": [],
        "resultados_sucesso": [],
        "resultados_falhas": [],
    }


def salvar_checkpoint(cp):
    cp["ultima_data"] = datetime.now().strftime("%Y-%m-%d")
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(cp, f, indent=2, ensure_ascii=False)


def main():
    print("=== EMAIL SENDER CONCEITO ===")
    print("A carregar checkpoint...")
    cp = carregar_checkpoint()

    hoje = datetime.now().strftime("%Y-%m-%d")
    if cp["ultima_data"] != hoje:
        cp["enviados_hoje"] = 0
        print("Novo dia — contador diário resetado.")
    else:
        resto = LIMITE_DIARIO - cp["enviados_hoje"]
        print(f"Já enviados hoje: {cp['enviados_hoje']} | Restante: {resto}")

    print(f"Limite diário: {LIMITE_DIARIO} | Intervalo: {INTERVALO_MIN}-{INTERVALO_MAX}s")
    print(f"Total histórico: {cp['total_enviados']} emails enviados\n")

    print("A carregar base de dados...")
    df = pd.read_excel(ARQUIVO_ENTRADA)

    try:
        for index, row in df.iterrows():
            if cp["enviados_hoje"] >= LIMITE_DIARIO:
                print(f"\nLimite diário de {LIMITE_DIARIO} emails atingido.")
                break

            nome_empresa = row.get("nome_empresa", "Empresa")
            descricao = row.get("descricao", "")
            emails_str = str(row.get("emails", "[]"))
            telefones = str(row.get("telefones", "[]"))

            try:
                emails = ast.literal_eval(emails_str)
            except:
                emails = []

            if not emails:
                print(f"[{index}] Sem email: {nome_empresa}")
                cp["resultados_falhas"].append(
                    {
                        "Empresa": nome_empresa,
                        "Telefones": telefones,
                        "Status": "Sem Email Cadastrado",
                    }
                )
                salvar_checkpoint(cp)
                continue

            emails_pendentes = [e for e in emails if e not in cp["emails_enviados"]]
            if not emails_pendentes:
                print(f"[{index}] Todos os emails de {nome_empresa} já enviados.")
                continue

            print(
                f"\n[{index}] A processar: {nome_empresa} "
                f"({len(emails)} email(s), {len(emails_pendentes)} pendente(s))"
            )

            texto_email = gerar_email_ia(nome_empresa, descricao)
            if not texto_email:
                print(f"[{index}] Erro na IA ao gerar texto para {nome_empresa}")
                for e in emails_pendentes:
                    cp["resultados_falhas"].append(
                        {
                            "Empresa": nome_empresa,
                            "Email_Tentado": e,
                            "Status": "Erro ao gerar texto com IA",
                        }
                    )
                salvar_checkpoint(cp)
                continue

            assunto = f"Parceria logística para a {nome_empresa}"

            for email_alvo in emails_pendentes:
                if cp["enviados_hoje"] >= LIMITE_DIARIO:
                    print(f"\nLimite diário de {LIMITE_DIARIO} emails atingido.")
                    break

                print(f"   -> A enviar para: {email_alvo}")
                enviado = enviar_email('joaoalexandrems3000@gmail.com', assunto, texto_email)

                if enviado:
                    cp["emails_enviados"].append(email_alvo)
                    cp["enviados_hoje"] += 1
                    cp["total_enviados"] += 1
                    cp["resultados_sucesso"].append(
                        {
                            "Empresa": nome_empresa,
                            "Email_Enviado": email_alvo,
                            "Texto_Gerado": texto_email,
                            "Status": "Enviado com Sucesso",
                        }
                    )
                    salvar_checkpoint(cp)

                    intervalo = random.randint(INTERVALO_MIN, INTERVALO_MAX)
                    print(f"   Aguardando {intervalo}s para não acionar o Anti-Spam...")
                    time.sleep(intervalo)
                else:
                    cp["resultados_falhas"].append(
                        {
                            "Empresa": nome_empresa,
                            "Email_Tentado": email_alvo,
                            "Status": "Erro no envio SMTP",
                        }
                    )
                    salvar_checkpoint(cp)

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Progresso salvo.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
    finally:
        salvar_checkpoint(cp)
        print("\nA guardar relatório Excel...")
        df_sucesso = pd.DataFrame(cp["resultados_sucesso"])
        df_falhas = pd.DataFrame(cp["resultados_falhas"])
        with pd.ExcelWriter(ARQUIVO_SAIDA, engine="openpyxl") as writer:
            if not df_sucesso.empty:
                df_sucesso.to_excel(writer, sheet_name="Emails_Enviados", index=False)
            if not df_falhas.empty:
                df_falhas.to_excel(writer, sheet_name="Pendencias_Contatos", index=False)
        print(f"Relatório salvo: {ARQUIVO_SAIDA}")
        print(f"\nResumo da sessão:")
        print(f"  - Enviados hoje: {cp['enviados_hoje']}")
        print(f"  - Total histórico: {cp['total_enviados']}")
        print(f"  - Pendências acumuladas: {len(cp['resultados_falhas'])}")
        print("Processo finalizado!")
