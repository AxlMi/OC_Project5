#! /usr/bin/env python
# coding: utf-8
import mysql.connector
from Create_database import Database
from Constant import *
from Create_database import *

class Menu:
    def __init__(self):
        self.db = Database()
        self.list_aliment = []
        self.choice = None
        self.choice_categorie = None
        self.choice_alim = None
        self.last_choice = None


    def select_choice(self):
        while self.choice is None:
            self.choice = input("1 - Remplacer un aliment ?\n2 - Retrouver mes aliments substitués. \n0 - quitter le programme\n>>> ")
            try:
                self.choice = int(self.choice)
            except:
                print("vous n'avez pas entrez une valeur correspondante")
                self.choice = None
        return self.choice


    def select_categorie(self):
        while self.choice_categorie is None:
            self.choice_categorie = input(categ)
            try:
                self.choice_categorie = int(self.choice_categorie)
            except:
                print("vous n'avez pas entrez une valeur correspondante")
                self.choice_categorie = None
        return self.choice_categorie

    def display_list(self,):
        while self.choice_alim is None:
            self.db.connect_with_user(user_acc="StudentOF", passw="1Ksable$", db="openfoodfact")
            self.db.mycursor.execute("SELECT product_name FROM product WHERE categories LIKE %s ORDER BY RAND() LIMIT 8",
            (categories[str(self.choice_categorie)]+"%",))
            my_result = self.db.mycursor.fetchall()
            self.choice_list(my_result)

    def choice_list(self, result):
            aliment_nb = 2
            if len(result) == 0:
                print("pas d'aliments à afficher")
            else:
                self.list_aliment.append("Quitter")
                self.list_aliment.append("Autres")
                print("0 : Quitter\n\n1 : Autres\n")
                for x in result:
                    self.list_aliment.append(x)
                    print(aliment_nb,":", x,"\n")
                    aliment_nb +=1
                try:
                    self.choice_alim = int(input("choisissez l'aliment souhaité : >>> "))
                except:
                    print("entrez un nombre valide")
                    self.select_alim = None
                return self.choice_alim

    def display_aliment(self):
        self.db.connect_with_user(user_acc="StudentOF", passw="1Ksable$", db="openfoodfact")
        sql = "SELECT * FROM product WHERE product_name = %s LIMIT 1"
        var = (self.list_aliment[self.choice_alim])
        self.db.mycursor.execute(sql, var)
        myresult = self.db.mycursor.fetchall()
        for x in myresult:
            print(format_aliment.format(x[1],x[6],x[2],x[3],x[4]))
        self.last_choice = input("""1 - trouvez un substitut \n
                    2 - sauvegarder cet aliment \n
                    3 - revenir au menu principal \n""")

    def add_save(self):
        self.db.connect_with_user(user_acc="StudentOF", passw="1Ksable$", db="openfoodfact")
        

    def display_save(self):
        self.db.connect_with_user(user_acc="StudentOF", passw="1Ksable$", db="openfoodfact")
        self.db.mycursor.execute("SELECT product_name FROM product WHERE save_product =0 LIMIT 10")
        myresult = self.db.mycursor.fetchall()
        self.choice_list(myresult)

#test = Menu()
#test.display_save()