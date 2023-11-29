import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from home import authenticator, config
st.header(":robot_face: Powder!")
@st.cache  
def load_data():
    df = pd.read_csv("dataset/base.csv")
    return df

name, authentication_status, username = authenticator.login('Login', 'main')

if not authentication_status:
    st.error("Acesso negado. Por favor, faça login.")
    st.stop()  
#Config da página
if 'df_robo' not in st.session_state:
    st.session_state['df_robo'] = load_data()
df = st.session_state['df_robo']

st.title('Muffato vs Condor')
search_ean = st.text_input("Pesquisar por EAN")

#Filtra os dataframe por loja 
df_muffato = df[df["loja"] == "Muffato"]
df_condor = df[df["loja"] == "Condor"]

#Une os dataframe e reseta o index
common_eans = pd.merge(
    df_muffato, df_condor, on="ean_value", how="inner", 
    suffixes=('_muffato', '_condor')
).reset_index()

exclusive_muffato = pd.merge(df_muffato, df_condor, on="ean_value", how="left", suffixes=('_muffato', '_condor'), indicator=True)
exclusive_muffato = exclusive_muffato[exclusive_muffato['_merge'] == 'left_only']
exclusive_muffato.drop(columns=[col for col in exclusive_muffato.columns if '_condor' in col] + ['_merge'], inplace=True)
exclusive_muffato.reset_index(drop=True, inplace=True)


common_eans['diff_percent'] = ((common_eans['Price_condor'] - common_eans['Price_muffato']) / common_eans['Price_condor'] * 100).fillna(0)

#st.write('Colunas em df:', common_eans.columns.tolist())


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
filtered_common_eans.reset_index(drop=True, inplace=True)
if search_ean:
    filtered_common_eans = filtered_common_eans[filtered_common_eans['ean_value'].astype(str).str.contains(search_ean)].reset_index()
# Condição para mostrar o gráfico (Opcional)
average_muffato = filtered_common_eans['Price_muffato'].mean()
average_condor = filtered_common_eans['Price_condor'].mean()
average_percent = ((average_condor - average_muffato) / average_condor * 100)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Média de preço Muffato", value=f"R${average_muffato:.2f}")
with col2:
    st.metric(label="Média de preço Condor", value=f"R${average_condor:.2f}")
with col3:
    st.metric(label="Diferença percentual", value=f"{average_percent:.2f}%")
display_comparison = st.checkbox('Mostrar gráfico')
if display_comparison:

    
    # Inicia a fig
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
            hovertext=filtered_common_eans['ean_value'],
            textfont=dict(size=26)
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
            textfont=dict(size=26)
        )
    )
  
    fig.update_layout(
        title='Comparação Muffato e Condor',
        xaxis=dict(
            type='category',
            tickvals=filtered_common_eans['ean_value'].tolist(),
            ticktext=[name[:40] for name in filtered_common_eans['Product Name_muffato'].tolist()],
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
    # Anotação da diferença percentual
    for idx, row in filtered_common_eans.iterrows():
        fig.add_annotation(
            x=idx, 
            y=max(row['Price_condor'], row['Price_muffato']),
            text=f"{row['diff_percent']:.2f}%",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-50,  # Ajuste conforme necessário para a posição y
            font=dict(
                size=14,
                family='Arial, sans-serif',
                color='green'
            )
        )
    #Exibe o gráfico
    st.plotly_chart(fig, use_container_width=True)

#Seleciona as coluna para exibir na base filtrada
columns_mandc = ['ean_value', 'Product Name_muffato', 'Product Name_condor', 'Price_condor', 
                 'Price_muffato', 'diff_percent', 'loja_muffato','loja_condor', 'brand_condor', 
                 'Departament_condor', 'Category_condor','SubCategory_condor','link_muffato']

st.title('Base')
st.markdown("-- baseado no filtro aplicado no gráfico")
filtered_common_eans['ean_value'] = filtered_common_eans['ean_value'].astype(str)
exclusive_muffato['ean_value'] = exclusive_muffato['ean_value'].astype(str)
st.dataframe(filtered_common_eans[columns_mandc],
             column_config={
                 "diff_percent": st.column_config.ProgressColumn(
                     "diff_percent", format="%d", min_value=-100, max_value=100
                 ),
             })


columns_m = ["Product Name_muffato", "ean_value",
             "link_muffato", 'Price_muffato','loja_muffato', 
           ]

st.title('Ativos somente no Muffato')

st.dataframe(exclusive_muffato[columns_m])
