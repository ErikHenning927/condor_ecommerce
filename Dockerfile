# Use uma imagem base Python
FROM python:3.9-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Instale as dependências necessárias
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie os arquivos do projeto para o diretório de trabalho
COPY . /app

# Exponha a porta que o Streamlit usará
EXPOSE 16549

# Comando para rodar o aplicativo Streamlit 
CMD ["./start.sh"]

