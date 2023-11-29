#!/bin/bash
pip install -r requirements.txt
# Instalar dependências

# Executar o aplicativo Streamlit
streamlit run home.py --server.enableWebsocketCompression=false



