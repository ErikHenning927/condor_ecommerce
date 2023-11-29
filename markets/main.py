from markets.muffato import *
from markets.festval import *
from markets.dataframes import *
from markets.condoremcasa import *
from markets.promo_muffato import *
import schedule
import time
from datetime import datetime

def scrap():
        festval(url_list)
        print("Festval processado!")
        end_url = "?sc=13&utmi_cp=161012023103032400&O=OrderByTopSaleDESC"
        url_list_m = [
                
                f"https://www.supermuffato.com.br/bazar/casa-e-cozinha/{end_url}",
                f"https://www.supermuffato.com.br/bazar/churrasco/{end_url}",
                f"https://www.supermuffato.com.br/bazar/descartaveis/{end_url}",
                f"https://www.supermuffato.com.br/bazar/lampadas-e-pilhas/{end_url}",
                f"https://www.supermuffato.com.br/bazar/duchas-e-chuveiros/{end_url}",
                f"https://www.supermuffato.com.br/bazar/ferramentas/{end_url}",
                f"https://www.supermuffato.com.br/bazar/papelaria/{end_url}",
                f"https://www.supermuffato.com.br/bazar/automotivo/{end_url}",
                f"https://www.supermuffato.com.br/bazar/linha-infantil/{end_url}",
                f"https://www.supermuffato.com.br/bazar/cama-mesa-e-banho/{end_url}",
                f"https://www.supermuffato.com.br/bazar/lazer-e-camping/{end_url}",
                f"https://www.supermuffato.com.br/bebidas/bebidas-alcoolicas/{end_url}",
                f"https://www.supermuffato.com.br/bebidas/bebidas-nao-alcoolicas/{end_url}",
                f"https://www.supermuffato.com.br/bebidas/agua/{end_url}",
                f"https://www.supermuffato.com.br/bebidas/bebidas-nao-alcoolicas/aguas/{end_url}",
                f"https://www.supermuffato.com.br/bebidas/bebidas-nao-alcoolicas/bebidas-de-soja/{end_url}",
                f"https://www.supermuffato.com.br/bebidas/bebidas-nao-alcoolicas/chas-prontos/{end_url}",
                f"https://www.supermuffato.com.br/bebidas/bebidas-nao-alcoolicas/isotonicos-e-energeticos/{end_url}",
                f"https://www.supermuffato.com.br/bebidas/bebidas-nao-alcoolicas/refrigerantes/{end_url}",
                f"https://www.supermuffato.com.br/bebidas/bebidas-nao-alcoolicas/sucos-e-refrescos?/{end_url}",
                f"https://www.supermuffato.com.br/carnes-aves-e-peixes/carnes-bovinas/{end_url}",
                f"https://www.supermuffato.com.br/carnes-aves-e-peixes/carnes-suinas/{end_url}",
                f"https://www.supermuffato.com.br/carnes-aves-e-peixes/linguicas/{end_url}",
                f"https://www.supermuffato.com.br/carnes-aves-e-peixes/frango/{end_url}",
                f"https://www.supermuffato.com.br/carnes-aves-e-peixes/peixes-e-frutos-do-mar/{end_url}",
                f"https://www.supermuffato.com.br/carnes-aves-e-peixes/ovinos-e-aves/{end_url}",
                f"https://www.supermuffato.com.br/congelados/pratos-prontos/{end_url}",
                f"https://www.supermuffato.com.br/congelados/sorvetes/{end_url}",
                f"https://www.supermuffato.com.br/congelados/petiscos-e-empanados/{end_url}",
                f"https://www.supermuffato.com.br/congelados/hamburgueres/{end_url}",
                f"https://www.supermuffato.com.br/congelados/lanches-prontos/{end_url}",
                f"https://www.supermuffato.com.br/congelados/legumes-congelados/{end_url}",
                f"https://www.supermuffato.com.br/congelados/polpas-de-frutas/{end_url}",
                f"https://www.supermuffato.com.br/congelados/sobremesas/{end_url}",
                f"https://www.supermuffato.com.br/congelados/paes-de-alho/{end_url}",
                f"https://www.supermuffato.com.br/frios-e-laticinios/laticinios/{end_url}",
                f"https://www.supermuffato.com.br/frios-e-laticinios/manteigas-e-margarinas/{end_url}",
                f"https://www.supermuffato.com.br/frios-e-laticinios/requeijoes/{end_url}",
                f"https://www.supermuffato.com.br/frios-e-laticinios/queijos/{end_url}",
                f"https://www.supermuffato.com.br/frios-e-laticinios/embutidos/{end_url}",
                f"https://www.supermuffato.com.br/frios-e-laticinios/massas-frescas/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/cabelo/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/sabonetes/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/desodorantes/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/higiene-oral/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/barbearia-e-depilacao/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/facial/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/cuidados-pessoais/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/cremes-para-o-corpo/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/bronzeadores-e-filtro-solar/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/repelentes/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/higiene-infantil/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/maos-e-pes/{end_url}",
                f"https://www.supermuffato.com.br/higiene-e-beleza/higiene-intima/{end_url}",
                f"https://www.supermuffato.com.br/hortifruti/frutas/{end_url}",
                f"https://www.supermuffato.com.br/hortifruti/frutas-processadas/{end_url}",
                f"https://www.supermuffato.com.br/hortifruti/legumes/{end_url}",
                f"https://www.supermuffato.com.br/hortifruti/verduras/{end_url}",
                f"https://www.supermuffato.com.br/hortifruti/ovos/{end_url}",
                f"https://www.supermuffato.com.br/hortifruti/sucos/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/roupas/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/desodorizantes-para-banheiro/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/limpadores/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/detergentes/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/saponaceos/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/desinfetantes/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/inseticidas/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/purificadores-de-ar/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/ceras-e-lustra-moveis/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/alcool-e-removedores/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/utensilios-para-limpeza/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/sacos-e-lixeiras/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/papel-higienico/{end_url}",
                f"https://www.supermuffato.com.br/limpeza/agua-sanitaria/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/arroz/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/feijao/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/acucares/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/massas/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/oleos-e-azeites/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/farinaceos-e-amidos/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/cafes-e-chas/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/sopas-e-caldos/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/condimentos-e-conservas/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/pipocas/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/salgadinhos-e-snacks/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/biscoitos/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/matinais/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/sobremesas/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/doces-e-chocolates/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/orientais/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/alimentacao-infantil/{end_url}",
                f"https://www.supermuffato.com.br/mercearia-e-alimentos/mundo-saudavel/{end_url}",
                f"https://www.supermuffato.com.br/padaria/bolos-e-tortas/{end_url}",
                f"https://www.supermuffato.com.br/padaria/paes/{end_url}",
                f"https://www.supermuffato.com.br/padaria/panettones/{end_url}",
                f"https://www.supermuffato.com.br/pet-shop/caes/{end_url}",
                f"https://www.supermuffato.com.br/pet-shop/gatos/{end_url}",
                f"https://www.supermuffato.com.br/pet-shop/passaros-e-peixes/{end_url}",
                f"https://www.supermuffato.com.br/pet-shop/acessorios/{end_url}",
                f"https://www.supermuffato.com.br/pet-shop/higiene/{end_url}",      
                f"https://www.supermuffato.com.br/ofertas/{end_url}",
        ]
        muffato(url_list_m)
        print("Muffato processado!")
        condoremcasa()
        print("Condor processado!")
        make_dataframe()
        print("Dataframes criados!")
        promo_m()
        print("Promoções Muffato coletadas!")
        sched = datetime.now()
        print(f'Dados atualizados em {sched}')
       
scrap()
# schedule.every().day.at("21:03").do(scrap)
# while True:
#     print('Rodando')
#     schedule.run_pending()
#     time.sleep(60) 
# schedule.every(5).minutes.do(scrap)

# while True:
#     print('Rodando')
#     schedule.run_pending()
#     time.sleep(1)