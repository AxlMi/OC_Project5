#! /usr/bin/env python
# coding: utf-8
from create_database import *
import requests
import json
import mysql.connector
import threading
import os


class DownloadApi:

    def time_download(self, name, page):
        # to indicate the time of download
        if name == "Thread 1":
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")
            print("chargement en cours {} %, veuillez patienter..".format((page*100/self.page_thread)))

    def end_download(self, name):
        # to indicate the end of download
        if name == "Thread 1":
            os.system("cls")
            print("chargement terminé")

    def downapi(self, start, end, name):
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
                            'page_size': 100
                            })
            self.time_download(name, i)
            response = json.loads(products.text)
            if len(response) == 0:
                print("fin du telechargement")
                break
            # this condition makes it possible not to take the empty informatio
            for product in response['products']:
                if product.get("stores") is not None\
                and product.get("stores") != "":
                    self.fill_table("stores", "store", product.get('stores'))
                    if product.get("brands") is not None\
                    and product.get("brand") != "":
                        self.fill_table("brands", "brands", product.get('brands'))
                        if product.get("categories") is not None\
                        and product.get("categories") != "":
                            product_cat = product.get("categories")
                            product_cat = product_cat.split(",")
                            product_cat = ",".join(product_cat[:8])
                            self.fill_table("categories", "Categories", product_cat)
                            if product.get("product_name") is not None\
                            and product.get("nutrition_grade_fr")\
                            is not None and product.get("product_name") != ""\
                            and product.get("nutrition_grade_fr") != "":       
                                sql = """INSERT INTO product (
                                    Product_name,
                                    Categories_id,
                                    Nutrition_grade,
                                    Brands_id,
                                    Stores_id,
                                    url_product,
                                    save_product) VALUES (%s, %s, %s, %s, %s, %s, 0)"""
                                val = (
                                    product.get('product_name'),
                                    self.research_id("categories", "Categories", product_cat),
                                    product.get('nutrition_grade_fr'),
                                    self.research_id("brands", "brands", product.get('brands')),
                                    self.research_id("stores", "store", product.get('stores')),
                                    product['url'])
                                db.mycursor.execute(sql, val,)
                                db.mydb.commit()
        self.end_download(name)
        db.mydb.close()

    def research_id(self, table, column, value):
        db = Database()
        db.connect_with_user(
            user_acc="StudentOF",
            passw="1Ksable$",
            db="openfoodfact")
        try:
            db.mycursor.execute("SELECT ID FROM " + table + " WHERE " + column + " = %s", (value, ))
            my_result = db.mycursor.fetchone()
            return my_result[0]
        except TypeError:
            pass

    def fill_table(self, table, column, value):
        db = Database()
        db.connect_with_user(
            user_acc="StudentOF",
            passw="1Ksable$",
            db="openfoodfact")
        try:
            db.mycursor.execute("INSERT INTO " + table + " (" + column + ") VALUE (%s)", (value, ))
            db.mydb.commit()
        except mysql.connector.errors.IntegrityError:
            pass
        except mysql.connector.errors.DataError:
            pass

    """ this method will launch several threads to
        speed up the downloading of information.
        Need to indicate the number page at download
        and the number of threads you want to run"""
    def thread_api(self, number_page):
        nb_thread = 4
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
DAP.thread_api(500)
