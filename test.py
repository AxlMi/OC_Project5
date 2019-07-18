#! /usr/bin/env python
# coding: utf-8
from create_database import *
import requests
import json
import mysql.connector
import threading
import os

class DownloadApi:        

    def downapi(self, start, end, nom):
        self.db = Database()
        self.db.connect_with_user(
            user_acc="StudentOF",
            passw="1Ksable$",
            db="openfoodfact")
        for i in range(start, end):
            products = requests.get(
                        "https://world.openfoodfacts.org/cgi/search.pl", {
                            'action': 'process',
                            'tagtype_0': 'categories',  # categories selected
                            'tag_contains_0': 'contains',  # contains or not
                            'sort_by': 'unique_scans_n',
                            'countries': 'France',
                            'json': 1,
                            'page': i,
                            'page_size': 1000
                            })
            response = json.loads(products.text)
            self.fill_db(response)
    
    def fill_db(self, response):
        for product in response['products']:
            if product.get("product_name") is not None\
                and product.get("categories") is not None\
                and product.get("nutrition_grade_fr")\
                is not None and product.get("product_name")\
                != "" and product.get("categories") != ""\
                and product.get("nutrition_grade_fr") != "":
                product_cat = product.get("categories")
                product_cat = product_cat.split(",")
                product_cat = ",".join(product_cat[:8])
                self.fill_table("cat_product", "Categories", product_cat)
                sql = """INSERT INTO product (
                                Product_name,
                                Categories_id,
                                Nutrition_grade,
                                Brands,
                                Stores,
                                url_product,
                                save_product) VALUES (%s, %s, %s, %s, %s, %s, 0)"""
                val = (product.get('product_name'),
                    self.research_id("cat_product", "Categories", product_cat),
                    product.get('nutrition_grade_fr'),
                    product.get('brands'),
                    product.get('stores'),
                    product['url'])
                self.db.mycursor.execute(sql, val,)
                self.db.mydb.commit()
        
    def research_id(self, table, column, value):
        print(value)
        self.db.mycursor.execute("SELECT ID FROM " + table + " WHERE " + column + " = %s", (value, ))
        my_result = self.db.mycursor.fetchone()
        return my_result[0]

    def fill_table(self, table, column, value):
        try:
            self.db.mycursor.execute("INSERT INTO " + table + " (" + column + ") VALUE (%s)", (value, ))
            self.db.mydb.commit()
        except mysql.connector.errors.IntegrityError:
            pass
        except mysql.connector.errors.DataError:
            pass

    def thread_api(self, number_page):
        # choice the number of thread
        nb_thread = 8
        self.page_thread = int(number_page / nb_thread)
        index_start_thread = 0
        index_end_thread = self.page_thread
        for i in range(1, nb_thread):
            thread_downapi = threading.Thread(
                target=self.downapi,
                args=(
                    index_start_thread,
                    index_end_thread,
                    "Thread {}".format(i)))
            thread_downapi.start()
            index_start_thread += self.page_thread
            index_end_thread += self.page_thread

dap = DownloadApi()
dap.thread_api(100)

