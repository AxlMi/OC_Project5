import requests
import json

final_products = []


for i in range(1, 150):
    products = requests.get("https://world.openfoodfacts.org/cgi/search.pl",{
                'action': 'process',
                'tagtype_0': 'categories', #categories selected
                'tag_contains_0': 'contains', #contains or not
                'sort_by': 'unique_scans_n',
                'countries': 'France',
                'json': 1,
                'page': 553444000,
                'page_size' : 100
                })
    print(products.text)
    response = json.loads(products.text)

    for product in response['products']:
        # ajouter produits voulu sur sql
        final_products.append({
            'code': product['code']
        })