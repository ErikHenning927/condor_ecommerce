import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
def muffato(url_list_m):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    all_products = [] 
    
    for url_muffato in url_list_m:  
        page = requests.get(url_muffato, headers=headers)
        resposta = page.text
        #with open('muffa.html', 'w', encoding="utf-8") as f: f.write(page.content.decode("utf-8"))
        soup = BeautifulSoup(resposta, 'html.parser')
        products = soup.find_all('div', class_='prd-list-item')

        for product in products:
            image_tag = product.select_one('img')
            ean_value = ""
            if image_tag:
                ean_value = re.split('[_-]', image_tag.get('alt', '').strip())[0]

            price_tag = product.select_one('.prd-list-item-price-sell')
            price_value = ""
            if price_tag:
                price_value = price_tag.text.strip()
            if price_value:
                if (product.h3 != None) and (product.h3.get('class') != None):
                    cleaned_name = ' '.join(product.h3.text.split()).strip()
                    product_info = {
                        "Product Name": cleaned_name,
                        "link": product.find('a').get('href'),
                        "ean_value": ean_value,
                        "Price": price_value
                    }
                    all_products.append(product_info)  # Adiciona o produto à lista principal

    with open('json/muffato.json', 'w', encoding="utf-8") as json_file:
        json.dump(all_products, json_file, ensure_ascii=False, indent=4)

    return all_products

def muf():
    url_muffato = "https://www.supermuffato.com.br/?ref=logo"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    page = requests.get(url_muffato, headers=headers)
    resposta = page.text
    with open('muffa.html', 'w', encoding="utf-8") as f: f.write(page.content.decode("utf-8"))
    soup = BeautifulSoup(resposta, 'html.parser')
    grid_divs = soup.find_all("div", class_=lambda value: value and 'grid' in value)
    links = []
    for div in grid_divs:
        a_tag = div.find('a')
        if a_tag and a_tag.has_attr('href'):
            href = a_tag['href']
            img_tag = a_tag.find('img')
            promo = a_tag.find('alt')
            if img_tag and img_tag.has_attr('src'):
                url_img = "https://muffatosupermercados.vteximg.com.br"
                url_link = "https://www.supermuffato.com.br/"
                src = img_tag['src']
                promo = img_tag['alt']
                links.append({"href": f"{url_link}{href}", "src": f"{url_img}{src}", "promo": promo})
                with open('json/links.json', 'w', encoding='utf-8') as f:
                    json.dump(links, f, ensure_ascii=False, indent=4)
    



