# Use uma imagem base Python
FROM python:3.9-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Instale as dependências necessárias
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*


COPY . /app

RUN pip install -r requirements.txt


EXPOSE 16548


CMD ["streamlit", "run", "home.py", "--server.port=16548", "--server.address=0.0.0.0"]
