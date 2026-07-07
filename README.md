# Conceito Mail AI 🤖✈️

**Automação inteligente de e-mails comerciais com IA generativa.**

Este projeto automatiza o envio de e-mails de prospecção para uma base de contatos, utilizando inteligência artificial (Groq + Llama 3) para gerar textos personalizados para cada empresa, com template HTML profissional e imagens inline.

---

## Funcionalidades

- **Geração de texto com IA** — Cada empresa recebe um e-mail único, personalizado com base no nome e descrição do negócio
- **Template HTML profissional** — Layout responsivo, com logo, assinatura, CTA e rodapé
- **Imagens inline (CID)** — Logo e assinatura incorporadas diretamente no e-mail
- **Envio automático via SMTP** — Configurado para Hostinger, com pausas inteligentes anti-spam
- **Relatório em Excel** — Planilha com abas separadas para enviados e pendências

---

## Estrutura do Projeto

```
├── index.py              # Ponto de entrada
├── config.py             # Configurações via .env
├── ai_client.py          # Geração de texto com Groq
├── email_builder.py      # Template HTML do e-mail
├── smtp_client.py        # Envio SMTP com imagens inline
├── orchestrator.py       # Orquestração do fluxo completo
├── .env                  # Credenciais (não versionado)
├── .env.example          # Template de configuração
├── .gitignore
├── Branco (1).png        # Logo da empresa
├── assinatura.png        # Assinatura visual
└── expositores_extraidos_20260619_154022.xlsx  # Base de contatos
```

---

## Como usar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/conceito-mail-ai.git
cd conceito-mail-ai
```

### 2. Crie o ambiente virtual e instale as dependências

```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 3. Configure o arquivo `.env`

Copie o `.env.example` para `.env` e preencha com suas credenciais:

```env
GROQ_API_KEY=sua_chave_groq
EMAIL_REMETENTE=seu@email.com
SENHA_EMAIL=sua_senha
SMTP_SERVER=smtp.seuprovedor.com
SMTP_PORT=587
ARQUIVO_ENTRADA=planilha.xlsx
ARQUIVO_SAIDA=resultado_campanha.xlsx
```

### 4. Prepare a planilha de entrada

O arquivo Excel deve conter as colunas:
- `nome_empresa` — Nome da empresa
- `descricao` — Descrição do negócio (usada pela IA)
- `emails` — Lista de e-mails no formato `['email1@teste.com', 'email2@teste.com']`
- `telefones` — Telefones de contato (opcional)

### 5. Execute

```bash
python index.py
```

---

## Stack

- **Python 3.14+**
- **Groq API** — Inferência Llama 3.1 (8B)
- **Pandas** — Leitura/escrita de planilhas
- **SMTP (Hostinger)** — Envio de e-mails
- **python-dotenv** — Gerenciamento de variáveis de ambiente

---

## LinkedIn

> Projeto open source de automação comercial com IA. Ideal para equipes de vendas que querem escalar a prospecção sem perder a personalização.

[LinkedIn](https://www.linkedin.com/in/joão-alexandre-648ba224b/) • [Portfolio](https://joaoalexandre.vercel.app)

---

<p align="center">Feito com ☕ e Python</p>
