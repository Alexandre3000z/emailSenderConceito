from ai_client import gerar_email_ia
from smtp_client import enviar_email


EMPRESA = "Grupo Ouvidor"
EMAIL = "logistica@lojaouvidor.com.br"
DESCRICAO = (
    "O Grupo Ouvidor é uma tradicional rede cearense de design de interiores e decoração, "
    "com mais de 90 anos de história. Em Fortaleza, a empresa opera por meio de três espaços "
    "integrados (Móveis, Tecidos e Persianas) localizados na Av. Santos Dumont, no bairro Aldeota. "
    "Suas principais áreas de atuação são: Loja Ouvidor Móveis — Focada em mobiliário de alto padrão "
    "e objetos de arte. Ouvidor Tecidos — Trabalha com curadoria de tecidos finos nacionais e importados. "
    "Uniflex Ouvidor — Especializada em cortinas, persianas e toldos."
)


def main():
    print(f"Gerando texto para {EMPRESA}...")
    texto = gerar_email_ia(EMPRESA, DESCRICAO)
    if not texto:
        print("Erro ao gerar texto com IA.")
        return

    print(f"Texto gerado:\n{texto}")
    assunto = f"Parceria logística para a {EMPRESA}"
    enviado = enviar_email(EMAIL, assunto, texto)
    if enviado:
        print(f"Email enviado com sucesso para {EMAIL}!")
    else:
        print(f"Falha no envio para {EMAIL}.")


if __name__ == "__main__":
    main()
