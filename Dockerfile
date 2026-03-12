# Imagem base oficial do Python (leve)
FROM python:3.10-slim

# Definir diretório de trabalho dentro do contentor
WORKDIR /app

# Copiar ficheiro de dependências primeiro (para cache de camadas)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação
COPY . .

# Expor a porta do Streamlit
EXPOSE 8501

# Configurar Streamlit para não abrir o browser automaticamente
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Comando de arranque
CMD ["streamlit", "run", "app.py"]
