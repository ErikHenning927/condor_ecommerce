#!/bin/bash
pip install -r requirements.txt
# Instalar dependências

# Executar o aplicativo Streamlit
streamlit run home.py --server.port=16549 --server.address=0.0.0.0


