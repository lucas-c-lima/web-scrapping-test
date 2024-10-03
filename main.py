from bs4 import BeautifulSoup
import requests
import unidecode
import pandas as pd

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'
}

product = input('Produto: ')
product = unidecode.unidecode(product)
product = product.replace(' ', '-')

cont = 1
data = []
print('Carregando...')

while cont <= 50:
    url = f'https://lista.mercadolivre.com.br/{product}_Desde_{cont}_NoIndex_True'
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')

    items = soup.find_all('li', class_='ui-search-layout__item')

    if not items:
        continue

    for item in items:
        try:
            item_name = item.find('h2', class_='poly-box poly-component__title').text
            item_brand = item.find('span', class_='poly-component__brand')
            item_price = item.find('span', class_='andes-money-amount andes-money-amount--cents-superscript').text.replace('R$','').replace('.','')
            item_link = item.find('a')['href']

            data.append({
                'Nome' : item_name,
                'Marca' : item_brand.text if item_brand != None else "Não especificado",
                'Preço' : item_price,
                'Link' : item_link
            })

        except AttributeError:
            continue

    cont += 1

df = pd.DataFrame(data)
output_file = f'{product}_mercadolivre.xlsx'
df.to_excel(output_file, index=False)

print(f'Dados salvos em {output_file}')
