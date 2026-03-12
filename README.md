# ⚖️ Agente IA — Especialista em Contratos Administrativos

MVP de um agente de inteligência artificial especialista na **Lei 14.133/2021** (Nova Lei de Licitações e Contratos Administrativos). Permite fazer upload de uma planilha de contratos públicos e fazer perguntas em linguagem natural, obtendo respostas com embasamento jurídico.

> **Contexto estratégico:** Este projeto é um laboratório de validação técnica para RAG (*Retrieval-Augmented Generation*) e orquestração de agentes de IA num domínio de alta complexidade (legislação e contratos públicos), com portabilidade garantida via Docker.

---

## 🏗️ Arquitectura

```
app_agenteIA_teste/
├── .env                        # Chave da API OpenAI (não versionar)
├── .gitignore
├── app.py                      # Núcleo da aplicação (Streamlit + LangChain)
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Imagem do contentor
├── docker-compose.yml          # Orquestração do ambiente
└── dados_teste/
    └── contratos_teste.xlsx    # Planilha de exemplo (25 contratos fictícios)
```

### Stack Tecnológica

| Camada | Tecnologia | Função |
|---|---|---|
| Interface | [Streamlit](https://streamlit.io/) | Frontend web interativo com chat |
| Dados | [Pandas](https://pandas.pydata.org/) + [OpenPyXL](https://openpyxl.readthedocs.io/) | Leitura e manipulação da planilha |
| Orquestração IA | [LangChain](https://www.langchain.com/) | Criação e gestão do agente |
| LLM | [OpenAI GPT-4o](https://platform.openai.com/) | Modelo de linguagem do agente |
| Infraestrutura | [Docker](https://www.docker.com/) + Docker Compose | Contentorização e portabilidade |

---

## 🚀 Como Iniciar

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e Docker Compose instalados
- Uma chave de API da [OpenAI](https://platform.openai.com/api-keys)

### 1. Configurar a chave da API

Edite o ficheiro `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sk-sua-chave-real-aqui
```

### 2. Construir e iniciar o contentor

```bash
docker-compose up --build
```

Para execução em background (modo detached):

```bash
docker-compose up -d --build
```

### 3. Aceder à aplicação

Abra o browser em **[http://localhost:8501](http://localhost:8501)**.

---

## 💬 Como Usar

1. **Faça upload** da sua planilha de contratos (CSV, XLSX ou XLS) na barra lateral
2. **Visualize** a pré-visualização dos dados carregados
3. **Faça perguntas** em linguagem natural na caixa de chat

### Exemplos de perguntas

- *"Há contratos por dispensa de licitação com valores acima do limite do Art. 75?"*
- *"Quais contratos têm vigência superior a 5 anos?"*
- *"Resuma as modalidades de licitação presentes na planilha e os seus totais."*
- *"Existe algum contrato por inexigibilidade com valor abaixo de R$ 50.000?"*

---

## 🧠 O Agente — Persona e Competências

O agente é configurado com um **System Prompt** que define a sua persona como auditor especialista, instruindo-o a:

- Fundamentar respostas nos dispositivos legais da **Lei 14.133/2021**
- Verificar **conformidade de modalidades, valores e prazos** com os limites legais
- Destacar **alertas de inconformidade** e riscos jurídicos
- Apresentar análises quantitativas (totais, médias, filtros)
- Responder sempre em **Português do Brasil**

---

## 🗂️ Dados de Teste

O ficheiro `dados_teste/contratos_teste.xlsx` contém **25 registos fictícios** com as seguintes colunas:

| Coluna | Descrição |
|---|---|
| Nº Contrato | Identificador do contrato |
| Modalidade | Ex.: Pregão Eletrônico, Dispensa, Inexigibilidade |
| Objeto | Descrição do bem ou serviço contratado |
| Valor (R$) | Valor total do contrato |
| Órgão Contratante | Entidade pública contratante |
| CNPJ Contratado | CNPJ da empresa fornecedora |
| Empresa Contratada | Nome da empresa fornecedora |
| Data de Assinatura | Data de celebração do contrato |
| Vigência Início / Fim | Período de vigência contratual |
| Status | Vigente, Encerrado ou Rescindido |

---

## 🔧 Comandos Úteis

```bash
# Ver logs em tempo real
docker-compose logs -f

# Parar o contentor
docker-compose down

# Reiniciar após alterar o .env
docker-compose restart

# Reconstruir a imagem (após alterar requirements.txt)
docker-compose up --build
```

---

## 📋 Fluxo de Execução

```
Utilizador faz upload da planilha
        ↓
Pandas lê e cria o DataFrame em memória
        ↓
Utilizador digita uma pergunta
        ↓
LangChain envia pergunta + contexto jurídico (System Prompt) + DataFrame → OpenAI GPT-4o
        ↓
Agente gera código Pandas → executa → obtém resultados
        ↓
GPT-4o formula resposta jurídica e analítica
        ↓
Streamlit exibe a resposta no chat
```

---

## ⚠️ Segurança

- O ficheiro `.env` está incluído no `.gitignore` — **nunca versione a sua chave de API**
- O agente utiliza `allow_dangerous_code=True` para execução de código Pandas — use apenas em ambiente controlado
