import requests
import json
import re
import os


url_festval = f'https://www.festval.com/adega?page=10'

def export_html(url, output_file_path):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(output_file_path, 'w', encoding="utf-8") as f:
            f.write(response.text)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return response.status_code == 200

def extract_json_from_html(file_path, start_line, end_line):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return "".join(lines[start_line-1:end_line])

def extract_product_info(html_content):
    keys_of_interest = ['nameComplete', 'ean', 'Price', 'brand']
    pattern = re.compile(rf'("({"|".join(keys_of_interest)})":\s*(".*?"|\d+\.?\d*))', re.DOTALL)

    found_items = pattern.findall(html_content)
    products = []
    current_product = {}
    
    for item in found_items:
        key, value = item[1], json.loads(item[2])

        if key == 'ean':
            key = 'ean_value'
        elif key == 'nameComplete':
            key = 'Product Name'

        if key in current_product:
            products.append(current_product)
            current_product = {}

        current_product[key] = value

    if current_product:
        products.append(current_product)

    if not 'Product Name' in products:
        default_product = {
            'Product Name': 'não encontrado',
            'ean_value': 'não encontrado',
            'Price': 0,
            'ListPrice': 0,
            'brand': 'sem marca'
        }
        products.append(default_product)

    return products
def convert_price(price):
    if isinstance(price, str):
        return price.replace('R$', '').replace(',', '.')
    return price 

def festval(url_list):
    all_products = [] 

    for base_url in url_list:
        for page in range(1, 11):
            url = f"{base_url}?page={page}"
            html_file_path = f'festval_page_{page}.html'

            if export_html(url, html_file_path):
                html_content = extract_json_from_html(html_file_path, 131, 137)
                products_info = extract_product_info(html_content)

                for product in products_info:
                    if 'Price' in product:
                        product['Price'] = convert_price(product['Price'])

                all_products.extend(products_info)


                if os.path.exists(html_file_path):
                    os.remove(html_file_path)

    with open('json/festval.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_products, json_file, ensure_ascii=False, indent=4)

# Define the base URLs
url_list = [
    'https://www.festval.com/acougue',
    'https://www.festval.com/adega',
    'https://www.festval.com/bebida',
    'https://www.festval.com/casa-e-utilidades',
    'https://www.festval.com/Diet-Light',
    'https://www.festval.com/Frios-e-Laticinios',
    'https://www.festval.com/Higiene-e-Perfumaria',
    'https://www.festval.com/Hortifruti',
    'https://www.festval.com/Importados',
    'https://www.festval.com/Limpeza',
    'https://www.festval.com/Mercearia',
    'https://www.festval.com/Padaria',
    'https://www.festval.com/Petshop',
    'https://www.festval.com/Sorvete',
]

# festval(url_list)