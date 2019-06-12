#! /usr/bin/env python
# coding: utf-8

import requests
import json
import mysql.connector        

for i in range(1, 500):
    mydb = mysql.connector.connect(
        host="localhost",
        user='StudentOF',
        passwd='1Ksable$',
        database="openfoodfact")
    mycursor = mydb.cursor()
    
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

    response = json.loads(products.text)
    #with open("test1page.json", "w") as f:
     #   f.write(json.dumps(response, indent=4))


#    
    for product in response['products']:
#        #print(product['nutrition_grade_fr'])
        sql = "INSERT INTO product (Product_name, Categories, Nutrition_grade, Brands, Stores, url_product) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (product['product_name'], product['categories'], product.get('nutrition_grade_fr'), product['brands'], product['stores'], product['url'])
        mycursor.execute(sql, val)
        mydb.commit()

