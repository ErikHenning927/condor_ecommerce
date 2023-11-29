import plotly.graph_objects as go
import streamlit as st 
import pandas as pd
from home import authenticator, config
st.header(":robot_face: Powder!")
name, authentication_status, username = authenticator.login('Login', 'main')

if not authentication_status:
    st.error("Acesso negado. Por favor, faça login.")
    st.stop()  
# st.set_page_config(layout="wide", page_title="Muffato vs Festval")
try:
    df = st.session_state["df_robo"]
except KeyError:
    st.error("Erro: A base de dados não foi carregada corretamente. Por favor, retorne à Home e tente novamente.")
    st.stop()
st.title("Muffato vs Festval")

search_ean = st.text_input("Pesquisar por EAN")
df_festval = df[df["loja"] == "Festval"]
df_muffato = df[df["loja"] == "Muffato"]


common_eans = pd.merge(df_festval, df_muffato, on="ean_value", how="inner",
                       suffixes=('_festval', '_muffato')).reset_index()


common_eans['diff_percent'] = (
    (common_eans['Price_muffato'] - common_eans['Price_festval']) / 
    common_eans['Price_muffato'] * 100
)

filtered_common_eans = common_eans.copy()
selected_brand = st.sidebar.multiselect(
    'Selecione uma marca', 
    options=common_eans['brand_festval'].unique(),
    key='brand_select'
)

# Aplica o filtro de marca, se selecionado
if selected_brand:
    filtered_common_eans = filtered_common_eans[filtered_common_eans['brand_festval'].isin(selected_brand)].reset_index(drop=True)

sort_order = st.sidebar.selectbox(
    'Ordenar por diferença percentual',
    ['Padrão', 'Decrescente']
)
if sort_order == 'Decrescente':
    filtered_common_eans = filtered_common_eans.sort_values(by='diff_percent', ascending=False).reset_index()
#st.write('Colunas em df:', filtered_common_eans.columns.tolist())
if search_ean:
    filtered_common_eans = filtered_common_eans[filtered_common_eans['ean_value'].astype(str).str.contains(search_ean)].reset_index()

average_muffato = filtered_common_eans['Price_muffato'].mean()
average_festval = filtered_common_eans['Price_festval'].mean()
average_percent = ((average_festval - average_muffato) / average_festval * 100)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Média de preço Muffato", value=f"R${average_muffato:.2f}")
with col2:
    st.metric(label="Média de preço Festval", value=f"R${average_festval:.2f}")
with col3:
    st.metric(label="Diferença percentual", value=f"{average_percent:.2f}%")
display_comparison = st.checkbox('Mostrar gráfico')
if display_comparison:
    fig = go.Figure()
    # num_items_to_show = st.selectbox(
    #     "Selecione o número de itens para visualizar", 
    # [50, 100, 'Todos']
    # )

    #     # Filtrar o DataFrame com base na escolha do usuário
    # if num_items_to_show != 'Todos':
    #     filtered_common_eans = filtered_common_eans.head(num_items_to_show)
    fig.add_trace(
        go.Bar(
            x=filtered_common_eans['ean_value'],
            y=filtered_common_eans['Price_festval'],
            name='Festval',
            marker_color='green',
            text=[f'R${x:.2f}' for x in filtered_common_eans['Price_festval']],
            textposition='outside',
            hovertext=filtered_common_eans['Product Name_festval'],
            textfont=dict(size=24)
        )
    )

    # Adiciona a barra para Muffato
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


    fig.update_layout(
        title='Comparação Muffato e Festval',
        xaxis=dict(
            type='category',
            tickvals=filtered_common_eans['ean_value'].tolist(),
            ticktext=[name[:50] for name in filtered_common_eans['Product Name_festval'].tolist()],
            tickangle=-45,
            tickmode='array',
            # tickfont=dict(
            #     color='black'  
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
    for idx, row in filtered_common_eans.iterrows():
        fig.add_annotation(
            x=idx,  # Usando o índice da linha para o posicionamento x
            y=max(row['Price_festval'], row['Price_muffato']),
            text=f"{row['diff_percent']:.2f}%",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40, 
            font=dict(
                size=14,
                family='Arial, sans-serif',
                color='green'
            )
        )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
columns = [
    'Product Name_muffato', 'Product Name_festval', 'ean_value', 'Price_festval', 'Price_muffato',
    'diff_percent','brand_festval', 'link_muffato',  'loja_muffato','loja_festval',
    
]

st.title('Base')
st.markdown("-- baseado no filtro aplicado no gráfico")
filtered_common_eans['ean_value'] = filtered_common_eans['ean_value'].astype(str)

st.dataframe(filtered_common_eans[columns],
             column_config={
                 "diff_percent": st.column_config.ProgressColumn(
                     "diff_percent", format="%d", min_value=-100, max_value=100
                 ),
             })


# st.dataframe(filtered_common_eans)  

