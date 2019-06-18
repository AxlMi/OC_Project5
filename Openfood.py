#! /usr/bin/env python
# coding: utf-8
from DB import Database
import requests
import json
import mysql.connector        
import threading


class download_api:
    
    def downapi(self, start, end):
        db = Database()
        db.connect_with_user(user_acc="StudentOF", passw="1Ksable$", db="openfoodfact")
        for i in range(start, end):
            products = requests.get("https://world.openfoodfacts.org/cgi/search.pl",{
                        'action': 'process',
                        'tagtype_0': 'categories', #categories selected
                        'tag_contains_0': 'contains', #contains or not
                        'sort_by': 'unique_scans_n',
                        'countries': 'France',
                        'json': 1,
                        'page': i,
                        'page_size' : 1000
                        })
            print("Chargement {} %".format((i/end)*100))
            response = json.loads(products.text)
            for product in response['products']:
                #print(product['nutrition_grade_fr'])
                if product.get("product_name") is not None and product.get("categories") is not None and product.get("categories") != "":
                    sql = "INSERT INTO product (Product_name, Categories, Nutrition_grade, Brands, Stores, url_product) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (product.get('product_name'), product.get('categories'), product.get('nutrition_grade_fr'), product.get('brands'), product.get('stores'), product['url'])
                    db.mycursor.execute(sql, val)
                    db.mydb.commit()

                #with open("test1page.json", "w") as f:
            #    f.write(json.dumps(response, indent=4))

    def thread_api(self, number_page):
        nb_thread = 10
        page_thread = int(number_page / nb_thread)
        index_start_thread = 0
        index_end_thread = page_thread
        for i in range(1, nb_thread):
            thread_downapi = threading.Thread(target=self.downapi, args=(index_start_thread, index_end_thread))
            thread_downapi.start()
            index_start_thread += page_thread
            index_end_thread += page_thread
            print(index_end_thread)

        

DAP = download_api()
DAP.thread_api(1000)

