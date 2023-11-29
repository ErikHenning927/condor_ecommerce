import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from home import authenticator, config
st.header(":robot_face: Powder!")
name, authentication_status, username = authenticator.login('Login', 'main')

if not authentication_status:
    st.error("Acesso negado. Por favor, faça login.")
    st.stop()  

try:
    df = st.session_state["df_robo"]
except KeyError:
    st.error("Erro: A base de dados não foi carregada corretamente. Por favor, retorne à Home e tente novamente.")
    st.stop()
st.title('Produtos em comum em todos')
search_ean = st.text_input("Pesquisar por EAN")


df_muffato = df[df["loja"] == "Muffato"]
df_condor = df[df["loja"] == "Condor"]
df_festval = df[df["loja"] == "Festval"]

# Merge Muffato and Condor on 'ean_value'
common_eans_mc = pd.merge(df_muffato, df_condor, on='ean_value', how='inner', 
                          suffixes=('_muffato', '_condor')).reset_index()

# Now merge the result with Festval on 'ean_value'
common_eans = pd.merge(common_eans_mc, df_festval, on='ean_value', how='inner')

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
if search_ean:
    filtered_common_eans = filtered_common_eans[filtered_common_eans['ean_value'].astype(str).str.contains(search_ean)].reset_index()

average_festval = filtered_common_eans['Price'].mean()
average_condor = filtered_common_eans['Price_condor'].mean()
average_muffato = filtered_common_eans['Price_muffato'].mean()
#average_percent = ((average_condor - average_festval) / average_condor * 100)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Média de preço Festval", value=f"R${average_festval:.2f}")
with col2:
    st.metric(label="Média de preço Condor", value=f"R${average_condor:.2f}")
with col3:
    st.metric(label="Média de preço Muffato", value=f"R${average_muffato:.2f}")
display_comparison = st.checkbox('Mostrar gráfico')
if display_comparison:
    # num_items_to_show = st.selectbox(
    # "Selecione o número de itens para visualizar", 
    # [50, 100, 'Todos']
    # )

    # # Filtrar o DataFrame com base na escolha do usuário
    # if num_items_to_show != 'Todos':
    #     filtered_common_eans = filtered_common_eans.head(num_items_to_show)
    fig = go.Figure()
    
    #Muffato Bar
    fig.add_trace(
        go.Bar(
            x=filtered_common_eans['ean_value'],
            y=filtered_common_eans['Price_muffato'],
            name='Muffato',
            marker_color='red',
            text=[f'R${x:.2f}' for x in filtered_common_eans['Price_muffato']],
            textposition='outside',
            hovertext=filtered_common_eans['Product Name_muffato'],
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
            hovertext=filtered_common_eans['Product Name_condor'],
            textfont=dict(size=24)
        )
    )
    #Festval bar
    fig.add_trace(
        go.Bar(
            x=filtered_common_eans['ean_value'],
            y=filtered_common_eans['Price'],
            name='Festval',
            marker_color='green',
            text=[f'R${x:.2f}' for x in filtered_common_eans['Price']],
            textposition='outside',
            hovertext=filtered_common_eans['Product Name'],
            textfont=dict(size=24)
        )
    )
    #Atualiza o gráfico
    fig.update_layout(
        title='Comparação Muffato e Festval e Condor',
        xaxis=dict(
            type='category',
            tickvals=filtered_common_eans['ean_value'].tolist(),
            ticktext=[name[:50] for name in filtered_common_eans['Product Name_muffato'].tolist()],
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
        margin=dict(t=0),  # Aumenta a margem superior
        height=600 
    )
    st.plotly_chart(fig, use_container_width=True)

st.title('Base')
filtered_common_eans['ean_value'] = filtered_common_eans['ean_value'].astype(str)

st.markdown("-- baseado no filtro aplicado no gráfico")
columns = [
    'Product Name_muffato', 'Product Name_condor', 'Product Name', 'ean_value', 'Price_muffato', 
    'Price_condor', 'Price', 'brand_condor', 'Departament_condor', 'Category_condor', 'SubCategory_condor', 
    'brand', 'loja_muffato', 'loja_condor', 'loja', 'link_muffato', 
]
st.dataframe(filtered_common_eans[columns])  
