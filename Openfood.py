#! /usr/bin/env python
# coding: utf-8

import requests
import json
import mysql.connector

class import_db:

    def connect(self,):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user='StudentOF',
            passwd='1Ksable$',
            database="openfoodfact")
        self.mycursor = self.mydb.cursor()
        

    for i in range(1, 2):
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
    
        #def add_values(key, type_key, values, values_key)
         #   self.connect()
      #mycursor.execute("CREATE TABLE product (name VARCHAR(255), address VARCHAR(255))")

        
        response = json.loads(products.text)
        
        for product in response['products']:
            print(product['product_name'])
            #for key, values in product.items():
               # print('{} {}'.format(key, values))

        def create_table(self,):
            self.connect()
            mycursor.execute("CREATE TABLE product (name VARCHAR(255), address VARCHAR(255))")


    #with open('dataok.json', 'w') as f:
     #   f.write(y)

    #print(x)
    #with open('datatest.json', 'w')as f:
     #   f.write(json.dumps(products.text, indent=50))
   # response = json.loads(products.text)
    #print(response)
    #print(response)

    #for product in response['products']:
        # ajouter produits voulu sur sql
     #   final_products.append({
      #      'code': product['code']
       # })