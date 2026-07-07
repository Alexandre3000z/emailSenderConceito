import time
import ast
import pandas as pd

from config import ARQUIVO_ENTRADA, ARQUIVO_SAIDA
from ai_client import gerar_email_ia
from smtp_client import enviar_email


def main():
    print("A carregar base de dados...")

    df = pd.read_excel(ARQUIVO_ENTRADA)

    lista_sucesso = []
    lista_sem_email = []

    for index, row in df.iterrows():
        nome_empresa = row.get("nome_empresa", "Empresa")
        descricao = row.get("descricao", "")
        emails_str = str(row.get("emails", "[]"))
        telefones = str(row.get("telefones", "[]"))

        try:
            emails = ast.literal_eval(emails_str)
        except:
            emails = []

        if not emails:
            print(
                f"[{index}] ❌ Sem email: {nome_empresa}. Adicionado à lista de pendências."
            )
            lista_sem_email.append(
                {
                    "Empresa": nome_empresa,
                    "Telefones": telefones,
                    "Status": "Sem Email Cadastrado",
                }
            )
            continue

        print(
            f"\n[{index}] 🔄 A processar empresa: {nome_empresa} (Total de emails: {len(emails)})"
        )

        texto_email = gerar_email_ia(nome_empresa, descricao)

        if texto_email:
            print("   ⏳ Aguardando 2 segundos antes de enviar...")
            time.sleep(2)
            assunto = f"Parceria logística para a {nome_empresa}"

            for email_alvo in emails:
                print(f"   -> A enviar para: {email_alvo}")
                enviado = enviar_email(
                    "joaoalexandrems3000@gmail.com", assunto, texto_email
                )

                if enviado:
                    lista_sucesso.append(
                        {
                            "Empresa": nome_empresa,
                            "Email_Enviado": email_alvo,
                            "Texto_Gerado": texto_email,
                            "Status": "Enviado com Sucesso",
                        }
                    )

                    print(
                        f"   ⏳ Aguardando 60 segundos para não acionar o Anti-Spam..."
                    )
                    time.sleep(60)
                else:
                    lista_sem_email.append(
                        {
                            "Empresa": nome_empresa,
                            "Email_Tentado": email_alvo,
                            "Status": "Erro no envio SMTP",
                        }
                    )
        else:
            print(f"[{index}] ❌ Erro na IA ao gerar texto para {nome_empresa}")
            for email_alvo in emails:
                lista_sem_email.append(
                    {
                        "Empresa": nome_empresa,
                        "Email_Tentado": email_alvo,
                        "Status": "Erro ao gerar texto com IA",
                    }
                )

    print("\nA guardar relatórios...")
    df_sucesso = pd.DataFrame(lista_sucesso)
    df_falhas = pd.DataFrame(lista_sem_email)

    with pd.ExcelWriter(ARQUIVO_SAIDA, engine="openpyxl") as writer:
        if not df_sucesso.empty:
            df_sucesso.to_excel(writer, sheet_name="Emails_Enviados", index=False)
        if not df_falhas.empty:
            df_falhas.to_excel(writer, sheet_name="Pendencias_Contatos", index=False)

    print(f"Processo finalizado! Planilha guardada como: {ARQUIVO_SAIDA}")
