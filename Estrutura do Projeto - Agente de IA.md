# **Relatório de Estrutura do Projeto: Agente de IA Especialista em Contratos Administrativos**

## **1\. Visão Geral do Projeto**

Este documento detalha a arquitetura de um Produto Mínimo Viável (MVP) para uma aplicação de inteligência artificial baseada em contentores. O objetivo é permitir que o utilizador faça o carregamento (*upload*) de uma folha de cálculo (CSV ou Excel) contendo dados de contratações públicas e faça perguntas em linguagem natural.

A aplicação utiliza a API da OpenAI orquestrada para atuar com uma **persona específica**: um especialista na **Lei 14.133/2021 (Nova Lei de Licitações e Contratos Administrativos)** e legislações correlatas. A IA irá interpretar as perguntas, cruzar com os dados da folha de cálculo e responder com base no rigor jurídico exigido pela lei.

**Contexto Estratégico:** Este projeto serve como um laboratório avançado de validação técnica para o desenvolvimento futuro de um agente de apoio ao cliente (como o *bot* planeado para o Mercado Livre). Ao testar a IA num domínio de alta complexidade (legislação e contratos públicos), validamos a precisão do *Retrieval-Augmented Generation* (RAG) e a capacidade da IA de seguir regras de negócio estritas. Tudo isto com a garantia de portabilidade através de Docker.

## **2\. Árvore de Ficheiros e Diretórios (File Structure)**

A estrutura utiliza Docker para a sua contentorização, garantindo que o projeto é independente do sistema operativo.

meu-agente-contratos/  
│  
├── .env                  \# Variáveis de ambiente (a sua chave da OpenAI vai aqui \- NÃO versionar)  
├── .gitignore            \# Ficheiro para ignorar itens no controlo de versão  
├── app.py                \# Código principal da aplicação (Interface \+ Lógica do Agente Especialista)  
├── requirements.txt      \# Lista de dependências e bibliotecas do projeto  
├── Dockerfile            \# Receita para construir a imagem do contentor da aplicação  
├── docker-compose.yml    \# Orquestração do ambiente, mapeamento de portas e volumes  
└── dados\_teste/          \# Pasta para guardar folhas de cálculo de exemplo  
    └── contratos\_teste.xlsx \# Exemplo com colunas: Modalidade, Valor, Vigência, Objeto, etc.

## **3\. Detalhamento dos Componentes**

### **3.1. app.py (O Núcleo da Aplicação)**

Este ficheiro conterá toda a lógica do nosso MVP, com destaque para a injeção do contexto jurídico:

* **Frontend (Streamlit):**  
  * Renderiza o título da página e o contexto ("Especialista em Lei 14.133/2021").  
  * Cria uma área para carregamento do ficheiro de contratos (st.file\_uploader).  
  * Exibe o histórico de *chat* (st.chat\_message).  
  * Fornece a caixa de texto para as perguntas.  
* **Processamento de Dados (Pandas):**  
  * Recebe o ficheiro em memória do frontend.  
  * Transforma-o num *DataFrame* estruturado.  
* **Orquestração de IA (LangChain \+ OpenAI):**  
  * Inicializa o modelo de linguagem (LLM).  
  * **Injeção de Persona (System Prompt):** Configura o agente com instruções rigorosas, por exemplo: *"Atue como um auditor especialista em contratos administrativos focado na Lei 14.133/2021. Ao analisar os dados fornecidos, indique se as modalidades de licitação, prazos de vigência ou valores de dispensa estão em conformidade com a legislação aplicável..."*  
  * Cria o agente (create\_pandas\_dataframe\_agent) conectando o LLM ao DataFrame com este contexto ativo.  
  * Recebe a pergunta do utilizador, analisa os dados e formula a resposta jurídica e quantitativa.

### **3.2. requirements.txt (Dependências)**

O contentor Docker instalará estas bibliotecas de forma isolada:

streamlit==1.32.0       \# Para a interface web  
pandas==2.2.1           \# Para leitura e manipulação da folha de cálculo  
openpyxl==3.1.2         \# Motor para ler ficheiros .xlsx  
langchain==0.1.13       \# Framework de orquestração do agente  
langchain-openai==0.1.1 \# Integração específica LangChain \<-\> OpenAI  
langchain-experimental  \# Contém o agente de Pandas

### **3.3. Dockerfile (A Receita do Contentor)**

* Utiliza uma imagem base oficial do Python (ex: python:3.10-slim).  
* Copia o código e o ficheiro requirements.txt para dentro do contentor.  
* Instala as dependências.  
* Expõe a porta 8501\.  
* Define o comando de arranque (CMD \["streamlit", "run", "app.py"\]).

### **3.4. docker-compose.yml (A Orquestração)**

* Define o serviço app.  
* Mapeia a porta 8501\.  
* Injeta as variáveis de segurança do ficheiro .env no contentor.  
* Mapeia um volume para *hot-reloading* do código durante o desenvolvimento.

### **3.5. .env (Segurança)**

OPENAI\_API\_KEY=sk-sua-chave-secreta-aqui

## **4\. Fluxo de Execução (Data Flow)**

1. O utilizador inicia o ambiente executando o comando: docker-compose up \--build  
2. A interface web fica disponível no navegador local em http://localhost:8501.  
3. O utilizador faz o carregamento de contratos\_teste.xlsx.  
4. O Pandas lê o ficheiro e cria a tabela na memória do contentor.  
5. O utilizador digita: *"Verifique nesta planilha se há contratos firmados por dispensa de licitação cujos valores ultrapassam o limite estipulado no Art. 75 da Lei 14.133/2021 para compras em geral."*  
6. O Streamlit envia o texto e o contexto da "persona especialista" para o agente LangChain.  
7. O Agente (OpenAI) entende a regra legal (limite de valor atualizado), gera o código Pandas para filtrar os contratos de "dispensa" na tabela e avalia os valores.  
8. O Agente executa o código e obtém os resultados.  
9. A OpenAI formula uma resposta jurídica e analítica amigável, apontando eventuais inconformidades, e o Streamlit exibe o resultado no ecrã.

## **5\. Próximos Passos para Implementação**

1. **Criar a pasta do projeto** e os respetivos ficheiros (app.py, requirements.txt, Dockerfile, docker-compose.yml).  
2. **Inserir a chave da API** no ficheiro .env.  
3. **Desenvolver o Prompt do Especialista** no ficheiro app.py para garantir que o LLM responda estritamente sob a ótica administrativa/legal.  
4. **Construir e Iniciar o contentor** executando no terminal: docker-compose up \-d \--build  
5. **Testar a aplicação** acedendo a localhost:8501.