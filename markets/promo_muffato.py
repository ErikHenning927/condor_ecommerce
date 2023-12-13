import requests
from bs4 import BeautifulSoup
import re
import json

def promos_muffato(url_list_promo):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    all_products = [] 
    
    for promo_info in url_list_promo: 
        url_muffato = promo_info["href"] 
        page = requests.get(url_muffato, headers=headers)
        resposta = page.text
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
                        "Price": price_value,
                        "Image URL": promo_info["src"],  
                        "Alt Text": promo_info["alt"]   
                    }
                    all_products.append(product_info)

    with open('json/muffato_promo.json', 'w', encoding="utf-8") as json_file:
        json.dump(all_products, json_file, ensure_ascii=False, indent=4)

    return all_products

def is_valid_url(url):

    if not re.match(r'https?://', url):
        return False

    if url.count("https://www.supermuffato.com.br") > 1:
        return False
    return True
def get_links():
    url_muffato = "https://www.supermuffato.com.br/?ref=logo"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    page = requests.get(url_muffato, headers=headers)
    resposta = page.text
    soup = BeautifulSoup(resposta, 'html.parser')
    grid_divs = soup.find_all("div", class_=lambda value: value and 'grid' in value)
    links_info = []

    for div in grid_divs:
        a_tag = div.find('a')
        if a_tag and a_tag.has_attr('href'):
            href = a_tag['href']
            img_tag = div.find('img')
            if img_tag:
                src = img_tag.get('src', '')
                alt = img_tag.get('alt', '')
                end_url = "&sc=13&utmi_cp=241012023122643170"
                links_info.append({"href": f"https://www.supermuffato.com.br{href}{end_url}", "src": f"https://muffatosupermercados.vteximg.com.br{src}", "alt": alt})

    # Agora filtramos os links
    filtered_links_info = []
    for link in links_info:
        href = link['href']
        if is_valid_url(href):
            try:
                response = requests.head(href, timeout=5)
                if response.status_code == 200:
                    filtered_links_info.append(link)
            except requests.RequestException:
                pass  # Ignora URLs que causam exceção

    with open('json/links.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_links_info, f, ensure_ascii=False, indent=4)

    return filtered_links_info


file_path = 'json/links.json'
with open(file_path, 'r', encoding='utf-8') as file:
    links_info_updated = json.load(file)

def promo_m():
    
    links_info = get_links()

    file_path = 'json/links.json'

    with open(file_path, 'r', encoding='utf-8') as file:
        links_info_updated = json.load(file)

    all_products = promos_muffato(links_info_updated)

    return all_products

promo_m()