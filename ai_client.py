from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def gerar_email_ia(nome_empresa, descricao):
    prompt = f"""
    Você é um executivo de vendas da 'Conceito Cargas Aéreas', uma transportadora ágil que atende todo o território nacional.
    Sua missão é escrever um email comercial curto (máximo 3 parágrafos), amigável e personalizado para a empresa {nome_empresa}.
    
    Sobre a empresa cliente: {descricao}
    
    Regras:
    1. Crie conexão emocional elogiando o que eles fazem com base na descrição tentando ser sempre o mais claro e formal possivel.
    2. Ofereça os serviços da Conceito Cargas Aéreas de forma sutil, mostrando como a agilidade do transporte aéreo pode ajudar na logística dos produtos deles, lembrando que atendemos todo o território nacional, mas não atendemos internacionalmente.
    3. Finalize com uma chamada para ação (Call to Action) solicite que responda o email, nunca informe o telefone.
    4. Não use marcadores de posição genéricos, assine apenas como 'Atenciosamente Sarah Rebeca.'.
    5. Escreva diretamente o corpo do email, sem introduções suas.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você é um copywriter especialista em B2B focado em logística e transporte.",
                },
                {"role": "user", "content": prompt},
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Erro na IA para a empresa {nome_empresa}: {e}")
        return None
