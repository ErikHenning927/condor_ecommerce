import requests
from bs4 import BeautifulSoup
import json
value = "pet-shop"
# URL do site a ser raspado
url = f'https://www.supermuffato.com.br/{value}'

# Envia uma requisição GET para o site
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Analisa o conteúdo HTML da página
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Lista para armazenar os hrefs
    hrefs = []

    # Encontra todas as tags <h4> com a classe 'bebidas even'
    h4_tags = soup.find_all('h4', class_=f'{value} even')

    # Para cada tag <h4>, encontra a tag <a> aninhada e extrai o href
    for h4 in h4_tags:
        a_tag = h4.find('a')
        if a_tag and 'href' in a_tag.attrs:
            hrefs.append(a_tag['href'])

    # Encontra todas as tags <ul> com a classe 'bebidas-alcoolicas even'
    ul_tags = soup.find_all('ul', class_='bebidas-nao-alcoolicas even')

    # Para cada tag <ul>, encontra todas as tags <li> e extrai os hrefs das tags <a> aninhadas
    for ul in ul_tags:
        li_tags = ul.find_all('li')
        for li in li_tags:
            a_tag = li.find('a')
            if a_tag and 'href' in a_tag.attrs:
                hrefs.append(a_tag['href'])

    # Imprime os hrefs encontrados
    for href in hrefs:
        print(href)
else:
    print('Falha ao recuperar os dados')
