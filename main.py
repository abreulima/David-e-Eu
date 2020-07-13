import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

produtos = []
table = PrettyTable()
table.field_names = ["Especificacoes", "Preco", "Vendedor"]

for produto in produtos:
    print(produto["spec"])

page_count = 5

for i in range(1, page_count + 1):
    url = "https://www.boadica.com.br/pesquisa/multi_placavideo/precos?ClasseProdutoX=16&CodCategoriaX=0&XT=3&XE=2&XG=10%27).text&curpage="
    url = url + str(i)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    product_table = soup.find_all(class_='row preco detalhe')

    for el in product_table:

        price = el.find(class_='col-md-1 preco')
        price = price.text
        price = price.strip()

        spec = el.find(class_='col-md-4 center')
        spec = spec.text
        spec = spec.replace('\r\n', '').replace('\n', '').strip()
        spec = spec.replace("clique aqui e veja mais detalhes", "")

        seller = el.find(class_='modal-loja-dotnet')
        seller = seller.text
        seller = seller.replace('\r\n', '').replace('\n', '').strip()

        produto = {
            "spec" : spec,
            "price" : price,
            "seller" : seller
        }

        produtos.append(produto)

        short_spec =  spec[:36] + (spec[36:] and '..')
        table.add_row([short_spec, price, seller])

file = open("saida.txt", "w") 
file.write(table.get_string())
file.write("\nProdutos encontrados " + str(len(produtos)))
file.close()