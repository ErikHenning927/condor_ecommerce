import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
import yaml
from yaml.loader import SafeLoader

#from markets.main import *

st.header(":robot_face: Powder!")
with open('users/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
hashed_passwords = stauth.Hasher(['condor2023', 'condor2023']).generate()
def show_register_form():
    with st.form(key='register_form'):
        new_email = st.text_input('Email')
        new_username = st.text_input('Username')
        new_name = st.text_input('Name')
        new_password = st.text_input('Password', type='password')
        new_password_repeat = st.text_input('Repeat Password', type='password')
        submit_button = st.form_submit_button(label='Register')

        if submit_button:
            return new_email, new_username, new_name, new_password, new_password_repeat
    return None, None, None, None, None
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('Login', 'main')


if authentication_status:
    if username == "erik.henning":
        from markets.main import *
        if st.button('Processar Dados'):
            scrap()
    if username == 'henning':
        st.markdown('Caso não tenha usuário registre-se')
        email, username, name, password, password_repeat = show_register_form()
        if email and username and name and password and password_repeat:
            # Definição da Função de Hash
            def hash_password(password):
                hashed_password = stauth.Hasher([password]).generate()
                return hashed_password[0]

            # Função para Adicionar Usuário ao YAML
            def add_user_to_yaml(username, name, password, email):
                file_path = 'users/config.yaml'
                with open(file_path) as file:
                    config = yaml.safe_load(file)

                hashed_password = hash_password(password)

                config['credentials']['usernames'][username] = {
                    'email': email,
                    'name': name,
                    'password': hashed_password
                }

                with open(file_path, 'w') as file:
                    yaml.dump(config, file)
            # Validação e Registro de Usuário
            if password == password_repeat:
                add_user_to_yaml(username, name, password, email)
                st.write('Usuário criado com sucesso, faça login acima!')
            else:
                st.error("Passwords do not match.") 
    authenticator.logout('Logout', 'main')
    st.write(f'Bem Vindo *{name}*')


    # st.set_page_config(
    #     layout="wide",
    #     page_title="Data Search"
    # )
    
    @st.cache_data
    def load_data():
        df = pd.read_csv("dataset/base.csv")
        time.sleep(5)
        return df

    df = load_data()
    st.session_state["df_robo"] = df

    df_muffato = df[df["loja"] == "Muffato"]
    df_condor = df[df["loja"] == "Condor"]
    df_festval = df[df["loja"] == "Festval"]

    common_eans_mc = pd.merge(df_muffato, df_condor, on='ean_value', how='inner', suffixes=('_muffato', '_condor'))
    common_eans_mf = pd.merge(df_muffato, df_festval, on='ean_value', how='inner', suffixes=('_muffato', '_festval'))
    common_eans_cf = pd.merge(df_condor, df_festval, on='ean_value', how='inner', suffixes=('_condor', '_festval'))
    common_eans_mcf = pd.merge(common_eans_mc, df_festval, on='ean_value', how='inner')


    combined_df = pd.concat([common_eans_mc, common_eans_mf, common_eans_cf, common_eans_mcf]).reset_index(drop=True)
    unique_category = combined_df['Category_condor'].dropna().unique()
    unique_category.sort()  

    # Campo de seleção de categoria
    selected_category = st.selectbox("Escolha uma Categoria", unique_category)
    
    search_ean = st.text_input("Pesquisar por EAN")
    if st.button("Buscar"):

        category_df = combined_df[combined_df["Category_condor"] == selected_category]
        category_df['Price_muffato'] = category_df['Price_muffato'].fillna(0)
        category_df['Price_condor'] = category_df['Price_condor'].fillna(0)
        category_df['Price_festval'] = category_df['Price_festval'].fillna(0)

        average_muffato = category_df['Price_muffato'].mean()
        average_condor = category_df['Price_condor'].mean()
        average_festval = category_df['Price_festval'].mean()
        average_percent = ((average_condor - average_muffato) / average_condor * 100)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Média de preço Muffato", value=f"R${average_muffato:.2f}")
        with col2:
            st.metric(label="Média de preço Condor", value=f"R${average_condor:.2f}")
        with col3:
            st.metric(label="Média de preço Festval", value=f"R${average_festval:.2f}")
        # if not category_df.empty:
        #     columns = ['Product Name_condor','ean_value','Price_muffato','Price_condor','Price_festval', 'Price',
        #                'brand_condor','Departament_condor','Category_condor','SubCategory_condor',
        #                'Product Name_muffato','loja_muffato','loja_condor','loja_festval','Product Name_festval']
            

        #     st.write(category_df[columns])
        #     # st.write('Colunas em df:', category_df.columns.tolist())
        # else:
        #     st.write("Nenhum produto comum encontrado para a marca selecionada.")
        if search_ean:
            category_df = category_df[category_df['ean_value'].astype(str).str.contains(search_ean)].reset_index()
        fig = go.Figure()
        def format_bar_text(price_column):
            return [f'R${x:.2f}' if x != 0 else '' for x in price_column]
        # Muffato bar
        fig.add_trace(
            go.Bar(
                x=category_df['ean_value'],
                y=category_df['Price_muffato'],  
                name='Muffato',
                marker_color='red',
                text=format_bar_text(category_df['Price_muffato']),
                textposition='outside',
                hovertext=category_df['ean_value'],
                textfont=dict(size=24)
            )
        )

        # Condor bar
        fig.add_trace(
            go.Bar(
                x=category_df['ean_value'],
                y=category_df['Price_condor'], 
                name='Condor',
                marker_color='blue',
                text=format_bar_text(category_df['Price_condor']),
                textposition='outside',
                hovertext=category_df['ean_value'],
                textfont=dict(size=18)
            )
        )

        # Festval bar
        fig.add_trace(
            go.Bar(
                x=category_df['ean_value'],
                y=category_df['Price_festval'], 
                name='Festval',
                marker_color='green',
                text=format_bar_text(category_df['Price_festval']),
                textposition='outside',
                hovertext=category_df['ean_value'],
                textfont=dict(size=18)
            )
        )

        # Atualização do layout do gráfico
        fig.update_layout(
            title='Comparação de Preços entre Muffato, Condor e Festval',
            xaxis=dict(
                type='category',
                tickvals=category_df['ean_value'].tolist(),
                ticktext=[name[:30] for name in category_df['Product Name_condor'].tolist()],  # Ajuste conforme necessário
                tickangle=-45,
                tickmode='array',
                #tickfont=dict(color='black')
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


    st.header(":robot_face: Bases!")
    lojas = df["loja"].value_counts().index
    loja = st.sidebar.selectbox("loja", lojas)
    df_filtered = df[df["loja"] == loja]
    
   
    
    st.dataframe(df_filtered)  
    

elif authentication_status == False:
    st.error('Usuário ou senha incorretos')
elif authentication_status == None:
    st.warning('Por favor, digite usuário e senha!')

    
