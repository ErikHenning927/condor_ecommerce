import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from home import authenticator, config
st.header(":robot_face: Powder!")
# Função para carregar dados
@st.cache  
def load_data():
    df = pd.read_csv("dataset/base.csv")
    
    return df

name, authentication_status, username = authenticator.login('Login', 'main')
if not authentication_status:
    st.error("Acesso negado. Por favor, faça login.")
    st.stop()

# Carregamento de dados
if 'df_robo' not in st.session_state:
    st.session_state['df_robo'] = load_data()
df = st.session_state['df_robo']

st.title('Festval vs Condor')
search_ean = st.text_input("Pesquisar por EAN")
# Divisão do DataFrame por loja
df_festval = df[df["loja"] == "Festval"]
df_condor = df[df["loja"] == "Condor"]

# Junção de DataFrames para encontrar itens comuns e exclusivos
common_eans = pd.merge(df_festval, df_condor, on="ean_value", how="inner", suffixes=('_festval', '_condor')).reset_index()
exclusive_festval = pd.merge(df_festval, df_condor, on="ean_value", how="left", suffixes=('_festval', '_condor'), indicator=True)
exclusive_festval = exclusive_festval[exclusive_festval['_merge'] == 'left_only']
exclusive_festval.drop(columns=[col for col in exclusive_festval.columns if '_condor' in col] + ['_merge'], inplace=True)
exclusive_festval.reset_index(drop=True, inplace=True)

# Cálculo de diferença percentual
common_eans['diff_percent'] = ((common_eans['Price_condor'] - common_eans['Price_festval']) / common_eans['Price_condor'] * 100).fillna(0)

selected_department = st.sidebar.multiselect('Selecione um departamento', options=common_eans['Departament_condor'].unique(), key='department_select')

# Atualizando opções de categoria com base no departamento selecionado
if selected_department:
    categories = common_eans[common_eans['Departament_condor'].isin(selected_department)]['Category_condor'].unique()
else:
    categories = common_eans['Category_condor'].unique()
selected_category = st.sidebar.multiselect('Selecione uma categoria', options=categories, key='category_select')

# Atualizando opções de subcategoria e marca com base no departamento e na categoria selecionados
filtered_df = common_eans
if selected_department:
    filtered_df = filtered_df[filtered_df['Departament_condor'].isin(selected_department)]
if selected_category:
    filtered_df = filtered_df[filtered_df['Category_condor'].isin(selected_category)]
subcategories = filtered_df['SubCategory_condor'].unique()
brands = filtered_df['brand_condor'].unique()

selected_subcategory = st.sidebar.multiselect('Selecione uma subcategoria', options=subcategories, key='subcategory_select')
selected_brand = st.sidebar.multiselect('Selecione uma marca', options=brands, key='brand_select')
sort_order = st.sidebar.selectbox('Ordenar por diferença percentual', ['Padrão', 'Decrescente'])

# Função para aplicar filtros
def apply_filters(df):
    if selected_department:
        df = df[df['Departament_condor'].isin(selected_department)]
    if selected_category:
        df = df[df['Category_condor'].isin(selected_category)]
    if selected_subcategory:
        df = df[df['SubCategory_condor'].isin(selected_subcategory)]
    if selected_brand:
        df = df[df['brand_condor'].isin(selected_brand)]
    return df

filtered_common_eans = apply_filters(common_eans)

# Ordenação e cálculos de média
if sort_order == 'Decrescente':
    filtered_common_eans.sort_values(by='diff_percent', ascending=False, inplace=True)
if search_ean:
    filtered_common_eans = filtered_common_eans[filtered_common_eans['ean_value'].astype(str).str.contains(search_ean)].reset_index()
filtered_common_eans.reset_index(drop=True, inplace=True)

average_festval = filtered_common_eans['Price_festval'].mean()
average_condor = filtered_common_eans['Price_condor'].mean()
average_percent = ((average_condor - average_festval) / average_condor * 100)

# Exibição de métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Média de preço Festval", value=f"R${average_festval:.2f}")
with col2:
    st.metric(label="Média de preço Condor", value=f"R${average_condor:.2f}")
with col3:
    st.metric(label="Diferença percentual", value=f"{average_percent:.2f}%")

# Função para criar o gráfico de comparação
def create_comparison_figure(df):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=filtered_common_eans['ean_value'],
           
            y=filtered_common_eans['Price_festval'],
            name='Festval',
            marker_color='green',
            text=[f'R${x:.2f}' for x in filtered_common_eans['Price_festval']],
            textposition='outside',
            hovertext=filtered_common_eans['ean_value'],
            textfont=dict(size=24)
        )
    )
    #Condor bar
    fig.add_trace(
        go.Bar(
            x=filtered_common_eans['ean_value'],
            y=filtered_common_eans['Price_condor'],
            name='Condor',
            marker_color='blue',
            text=[f'R${x:.2f}' for x in filtered_common_eans['Price_condor']],
            textposition='outside',
            hovertext=filtered_common_eans['ean_value'],
            textfont=dict(size=24)
        )
    )
    #Atualiza o gráfico
    fig.update_layout(
        title='Comparação Festval e Condor',
        xaxis=dict(
            type='category',
            tickvals=filtered_common_eans['ean_value'].tolist(),  # Mantém os valores EAN como base para as posições
            ticktext=[name[:60] for name in filtered_common_eans['Product Name_festval'].tolist()],  # Trunca os nomes dos produtos para 20 caracteres
            tickangle=-45,
            tickmode='array',
            # tickfont=dict(
            # color='black' 
            # )
        ),
        yaxis=dict(
            title='Price'
        ),
        barmode='group',
        bargap=0.1,
        bargroupgap=0.05,
        margin=dict(t=20),  # Aumenta a margem superior
        height=600 
    )
    # Anotação da diferença percentual
    for idx, row in filtered_common_eans.iterrows():
        fig.add_annotation(
            x=idx,  # Usando o índice da linha para o posicionamento x
            y=max(row['Price_condor'], row['Price_festval']),
            text=f"{row['diff_percent']:.2f}%",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40,  # Ajuste conforme necessário para a posição y
            font=dict(
                size=14,
                family='Arial, sans-serif',
                color='green'
            )
        )
 
    return fig

# Exibição condicional do gráfico
display_comparison = st.checkbox('Mostrar gráfico')
if display_comparison:
    fig = create_comparison_figure(filtered_common_eans)
    st.plotly_chart(fig, use_container_width=True)

columns_candf = ["ean_value", "Product Name_festval","Price_festval","loja_festval",
"brand_festval","Product Name_condor","Price_condor","loja_condor","brand_condor",
"Departament_condor","Category_condor","SubCategory_condor", "diff_percent"]
columns_onlyf = [
    "Product Name_festval", "ean_value", "Price_festval", "loja_festval", "brand_festval",
]
# Exibição dos DataFrames
st.title('Base')
st.markdown("-- baseado no filtro aplicado no gráfico")
filtered_common_eans['ean_value'] = filtered_common_eans['ean_value'].astype(str)
exclusive_festval['ean_value'] = exclusive_festval['ean_value'].astype(str)

st.dataframe(filtered_common_eans[columns_candf])

st.title('Ativos somente no Festval')
st.dataframe(exclusive_festval[columns_onlyf])
