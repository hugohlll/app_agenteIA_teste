"""
Agente de IA Especialista em Contratos Administrativos
=====================================================
MVP utilizando Streamlit + LangChain + OpenAI

Este agente atua como um especialista na Lei 14.133/2021
(Nova Lei de Licitações e Contratos Administrativos),
analisando dados de contratações públicas fornecidos via
upload de folha de cálculo.
"""

import os
import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import (
    create_pandas_dataframe_agent,
)

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Agente Especialista em Contratos",
    page_icon="⚖️",
    layout="wide",
)

# ============================================================
# SYSTEM PROMPT — PERSONA DO ESPECIALISTA
# ============================================================
SYSTEM_PROMPT = """
Você é um auditor especialista em contratos administrativos, com profundo
conhecimento na Lei 14.133/2021 (Nova Lei de Licitações e Contratos
Administrativos) e legislações correlatas.

Ao analisar os dados fornecidos, siga estas diretrizes:

1. **Rigor Jurídico:** Sempre fundamente suas respostas nos dispositivos
   legais aplicáveis, citando artigos, incisos e parágrafos da Lei
   14.133/2021 quando pertinente.

2. **Análise de Conformidade:** Ao avaliar contratos, verifique:
   - Se as modalidades de licitação estão adequadas ao objeto e valor.
   - Se os prazos de vigência estão em conformidade com os limites legais.
   - Se os valores de dispensa e inexigibilidade respeitam os limites
     estipulados (Art. 75 e Art. 74).
   - Se as prorrogações contratuais observam os requisitos legais.

3. **Clareza e Objetividade:** Apresente suas análises de forma clara,
   organizada e acessível, mesmo para quem não é da área jurídica.

4. **Dados Quantitativos:** Quando possível, apresente valores, totais,
   médias e estatísticas relevantes extraídos da planilha.

5. **Alertas de Inconformidade:** Destaque claramente qualquer situação
   que possa representar uma irregularidade ou risco jurídico.

6. **Idioma:** Responda sempre em Português do Brasil.

Você tem acesso a um DataFrame do Pandas com os dados da planilha de
contratos. Use-o para responder às perguntas do utilizador com precisão.
"""


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================
def carregar_dados(ficheiro_upload) -> pd.DataFrame:
    """Carrega o ficheiro enviado pelo utilizador num DataFrame."""
    nome = ficheiro_upload.name.lower()
    if nome.endswith(".csv"):
        return pd.read_csv(ficheiro_upload)
    elif nome.endswith((".xlsx", ".xls")):
        return pd.read_excel(ficheiro_upload, engine="openpyxl")
    else:
        st.error("Formato não suportado. Envie um ficheiro CSV ou Excel.")
        return None


def criar_agente(df: pd.DataFrame):
    """Cria o agente LangChain conectado ao DataFrame."""
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
    )

    agente = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        allow_dangerous_code=True,
        agent_type="openai-tools",
        prefix=SYSTEM_PROMPT,
    )
    return agente


# ============================================================
# INTERFACE — CABEÇALHO
# ============================================================
st.title("⚖️ Agente Especialista em Contratos Administrativos")
st.markdown(
    """
    **Especialista na Lei 14.133/2021 — Nova Lei de Licitações e Contratos**

    Faça o upload de uma planilha com dados de contratações públicas e
    faça perguntas em linguagem natural. O agente irá analisar os dados
    sob a ótica da legislação vigente.
    """
)

st.divider()

# ============================================================
# INTERFACE — UPLOAD DE FICHEIRO
# ============================================================
with st.sidebar:
    st.header("📂 Dados de Contratos")
    ficheiro = st.file_uploader(
        "Carregue a sua planilha de contratos",
        type=["csv", "xlsx", "xls"],
        help="Formatos aceites: CSV, Excel (.xlsx / .xls)",
    )

    if ficheiro is not None:
        df = carregar_dados(ficheiro)
        if df is not None:
            st.success(f"✅ Ficheiro carregado: **{ficheiro.name}**")
            st.metric("Total de registos", len(df))
            with st.expander("🔍 Pré-visualização dos dados"):
                st.dataframe(df.head(10), use_container_width=True)
    else:
        df = None

    st.divider()
    st.caption(
        "💡 **Dica:** Pergunte sobre modalidades de licitação, "
        "valores de dispensa, prazos de vigência, conformidade legal, etc."
    )

# ============================================================
# INTERFACE — CHAT
# ============================================================

# Inicializar o histórico de mensagens na sessão
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Exibir o histórico de mensagens
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Verificar se a chave da API está configurada
api_key = os.getenv("OPENAI_API_KEY", "")
chave_valida = api_key and not api_key.startswith("sk-sua-chave")

# Caixa de entrada de perguntas
if pergunta := st.chat_input(
    "Faça uma pergunta sobre os contratos...",
    disabled=(df is None),
):
    if not chave_valida:
        st.error(
            "⚠️ **Chave da API OpenAI não configurada.** "
            "Insira a sua chave no ficheiro `.env` e reinicie o contentor."
        )
    elif df is None:
        st.warning("Por favor, carregue uma planilha primeiro.")
    else:
        # Adicionar a pergunta do utilizador ao histórico
        st.session_state.mensagens.append(
            {"role": "user", "content": pergunta}
        )
        with st.chat_message("user"):
            st.markdown(pergunta)

        # Processar a resposta do agente
        with st.chat_message("assistant"):
            with st.spinner("🔍 Analisando dados e legislação..."):
                try:
                    agente = criar_agente(df)
                    resposta = agente.invoke({"input": pergunta})
                    texto_resposta = resposta.get("output", str(resposta))
                except Exception as e:
                    texto_resposta = (
                        f"❌ Ocorreu um erro ao processar a pergunta:\n\n"
                        f"`{str(e)}`\n\n"
                        f"Verifique se a chave da API está correta e "
                        f"se o modelo está disponível."
                    )
                st.markdown(texto_resposta)

        # Adicionar a resposta ao histórico
        st.session_state.mensagens.append(
            {"role": "assistant", "content": texto_resposta}
        )

# Mensagem quando não há ficheiro carregado
if df is None:
    st.info(
        "👆 **Comece por carregar uma planilha de contratos** na barra "
        "lateral para ativar o chat com o agente especialista."
    )
