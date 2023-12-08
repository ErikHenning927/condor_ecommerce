import pandas as pd
import json

def condoremcasa():
    file = 'dataset/site-mercado-loja-21-20231208040928.csv'
    df = pd.read_csv(file, delimiter=';')
    df = df.dropna(axis=1, how='all')
    df.to_json('json/cec.json', orient='records', lines=False)
    
    json_structure = []
    for index, row in df.iterrows():
        json_structure.append({
            "Departament": row.iloc[1],
            "Category": row.iloc[2],
            "SubCategory": row.iloc[3],
            "brand": row.iloc[4],
            "ean_value": row.iloc[7],
            "Product Name": row.iloc[8],
            "Price": row.iloc[11]
        })
    with open('json/condoremcasa.json', 'w') as file:
        json.dump(json_structure, file, ensure_ascii=False, indent=4)

condoremcasa()