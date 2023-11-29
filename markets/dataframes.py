import pandas as pd
def convert_price(price):
    if isinstance(price, str):
        return price.replace('R$', '').replace(',', '.')
    return price 
def make_dataframe():
    muffato_df = pd.read_json('json/muffato.json')
    festval_df = pd.read_json('json/festval.json')
    condoremcasa_df = pd.read_json('json/condoremcasa.json')


    muffato_df['loja'] = 'Muffato'
    festval_df['loja'] = 'Festval'
    condoremcasa_df['loja'] = 'Condor'

    muffato_df['Price'] = muffato_df['Price'].apply(convert_price)
    festval_df['Price'] = festval_df['Price'].apply(convert_price)
    condoremcasa_df['Price'] = condoremcasa_df['Price'].apply(convert_price)

    combined_df = pd.concat([muffato_df, festval_df, condoremcasa_df], ignore_index=False)
    combined_df['Price'] = combined_df['Price'].astype(float)

    # Filtrar as linhas onde o preço não é 0.00
    filtered_df = combined_df[combined_df['Price'] != 0.00]
    

    filtered_df.to_csv('dataset/base.csv', index=False)

