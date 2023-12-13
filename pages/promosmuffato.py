import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from home import authenticator, config
st.header(":robot_face: Powder!")
try:
    df = st.session_state["df_robo"]
except KeyError:
    st.error("Erro: A base de dados não foi carregada corretamente. Por favor, retorne à Home e tente novamente.")
    st.stop()
name, authentication_status, username = authenticator.login('Login', 'main')
if not authentication_status:
    st.error("Acesso negado. Por favor, faça login.")
    st.stop()
def convert_price(price):
    try:
        if isinstance(price, str):
            price = price.replace('R$', '').replace(',', '.').strip()
            return float(price) if price else 0.0
        return float(price)
    except ValueError:
        return 0.0 

promos_df = pd.read_json('json/muffato_promo.json')
df_condor = df[df["loja"] == "Condor"]
promos_df['Price'] = promos_df['Price'].apply(convert_price)
df_condor['Price'] = df_condor['Price'].apply(convert_price)

promos_df.to_csv('dataset/promo.csv', index=False)

st.title('Promoções Muffato')
common_eans = pd.merge(promos_df, df_condor, on="ean_value", how="inner",
                       suffixes=('_muffato', '_condor')).reset_index()
common_eans['diff_percent'] = ((common_eans['Price_condor'] - common_eans['Price_muffato']) / common_eans['Price_condor'] * 100).fillna(0)
#common_eans.to_excel('black.xlsx')
#filtered_common_eans = common_eans.copy()
filtered_common_eans = common_eans.drop_duplicates(subset='ean_value').reset_index(drop=True)

selected_brand = st.sidebar.multiselect(
    'Selecione uma promoção', 
    options=common_eans['Alt Text'].unique(),
    key='Alt Text'
)
if selected_brand:
    filtered_common_eans = filtered_common_eans[filtered_common_eans['Alt Text'].isin(selected_brand)].reset_index(drop=True)
    promos_df = promos_df[promos_df['Alt Text'].isin(selected_brand)].reset_index(drop=True)

average_muffato = filtered_common_eans['Price_muffato'].mean()
average_condor = filtered_common_eans['Price_condor'].mean()
average_percent = ((average_condor - average_muffato) / average_condor * 100)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Média de preço muffato", value=f"R${average_muffato:.2f}")
with col2:
    st.metric(label="Média de preço Condor", value=f"R${average_condor:.2f}")
with col3:
    st.metric(label="Diferença percentual", value=f"{average_percent:.2f}%")

# Função para criar o gráfico de comparação
columns = [
    'Product Name_muffato', 'ean_value', 'Price_muffato', 'Price_condor', 'diff_percent', 'Alt Text',
    'brand', 'Departament', 'Category', 'SubCategory', 'Image URL'

]

st.markdown('Produtos em comum')
st.dataframe(filtered_common_eans[columns])


st.markdown('Promoções Muffato!')
st.dataframe(promos_df)

