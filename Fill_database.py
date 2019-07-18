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
        db = Database()
        db.connect_with_user(
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
            # to indicate the time of download
            if nom == "Thread 1":
                if os.name == "nt":
                    os.system("cls")
                else:
                    os.system("clear")
                print("chargement en cours {} %, veuillez patienter..".format((i*100/self.page_thread)))
            response = json.loads(products.text)
            # this condition makes it possible not to take the empty informatio
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
                    try:
                        db.mycursor.execute("INSERT INTO cat_product (Categories)\
                            VALUES (%s)", (product_cat, ))
                        db.mydb.commit()
                    except mysql.connector.errors.IntegrityError:
                        pass
                    except mysql.connector.errors.DataError:
                        continue
                    db.mycursor.execute("SELECT ID\
                        FROM cat_product\
                        WHERE Categories = %s", (product_cat, ))
                    my_result = db.mycursor.fetchone()
                    sql = """INSERT INTO product (
                        Product_name,
                        Categories_id,
                        Nutrition_grade,
                        Brands,
                        Stores,
                        url_product,
                        save_product) VALUES (%s, %s, %s, %s, %s, %s, 0)"""
                    val = (
                        product.get('product_name'),
                        my_result[0],
                        product.get('nutrition_grade_fr'),
                        product.get('brands'),
                        product.get('stores'),
                        product['url'])
                    db.mycursor.execute(sql, val,)
                    db.mydb.commit()
        # to indicate the end of download
        if nom == "Thread 1":
            os.system("cls")
            print("chargement terminé")
            db.mydb.close()

    """ this method will launch several threads to
        speed up the downloading of information.
        Need to indicate the number page at download
        and the number of threads you want to run"""
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


DAP = DownloadApi()
DAP.thread_api(100)
