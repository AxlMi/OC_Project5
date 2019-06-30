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
        self.choice = None
        while self.choice is None:
            self.choice = input("1 - Remplacer un aliment ?\n2 - Retrouver mes aliments favoris. \n0 - quitter le programme\n>>> ")
            try:
                self.choice = int(self.choice)
            except:
                print("vous n'avez pas entrez une valeur correspondante")
                self.choice = None
            return self.choice


    def select_categorie(self):
        self.choice_categorie = None
        while self.choice_categorie is None:
            self.choice_categorie = input(categ)
            try:
                self.choice_categorie = int(self.choice_categorie)
            except:
                print("vous n'avez pas entrez une valeur correspondante")
                self.choice_categorie = None
        return self.choice_categorie

    def display_list(self,):
        self.choice_alim = None
        while self.choice_alim is None:
            self.db.connect_with_user(user_acc="StudentOF", passw="1Ksable$", db="openfoodfact")
            self.db.mycursor.execute("SELECT product_name FROM product WHERE categories LIKE %s ORDER BY RAND() LIMIT 8",
            (categories[str(self.choice_categorie)]+"%",))
            my_result = self.db.mycursor.fetchall()
            self.choice_list(my_result)

    def choice_list(self, result):
        self.list_aliment = []
        self.choice_alim = None
        self.list_aliment.append("Quitter")
        self.list_aliment.append("Autres")
        print("0 : Quitter\n\n1 : Autres\n")
        aliment_nb = 2
        if len(result) == 0:
            print("pas d'aliments à afficher")
        else:
            for x in result:
                self.list_aliment.append(x)
                print(aliment_nb,":", x,"\n")
                aliment_nb +=1
        try:
            self.choice_alim = int(input("Entrez le choix souhaité : >>> "))
        except:
            print("entrez un nombre valide")
            self.select_alim = None
        return self.choice_alim

    def display_aliment(self):
        self.db.connect_with_user(user_acc="StudentOF", passw="1Ksable$", db="openfoodfact")
        sql = "SELECT * FROM product WHERE product_name = %s LIMIT 1"
        var = (self.list_aliment[self.choice_alim])
        self.db.mycursor.execute(sql, var,)
        myresult = self.db.mycursor.fetchall()
        for x in myresult:
            print(format_aliment.format(x[1],x[6],x[2],x[3],x[4]))
            self.last_choice = input("""                    1 - trouvez un substitut \n
                    2 - sauvegarder cet aliment dans les favoris \n
                    3 - revenir au menu \n
                    4 - retirer l'aliment des favoris\n""")
            if self.last_choice == "1":
                self.substitute(x[2], x[0], x[1])
            elif self.last_choice == "2":
                self.modify_save(x[0], 1)
            elif self.last_choice == "4":
                self.modify_save(x[0], 0)

    def modify_save(self, product, favorites):
        self.db.connect_with_user(user_acc="StudentOF", passw="1Ksable$", db="openfoodfact")
        sql_update = """UPDATE product SET save_product = %s WHERE id = %s"""
        val_update = (favorites, product,)
        self.db.mycursor.execute(sql_update, val_update)
        self.db.mydb.commit()
        if favorites == 1:
            print("votre produit a été ajouté aux favoris")
        else:
            print("votre produit a été retiré des favoris")

    def list_other_aliment(self,):
        self.list_aliment[:] = [] # remove all list aliment
        name_aliment = input("quel aliment recherchez vous ?")
        print(self.list_aliment)
        self.db.connect_with_user(user_acc="StudentOF", passw="1Ksable$", db="openfoodfact")
        self.db.mycursor.execute("SELECT product_name FROM product WHERE product_name LIKE %s LIMIT 10", ("%"+name_aliment+"%",))
        my_result = self.db.mycursor.fetchall()
        self.choice_list(my_result)
        if self.choice_alim != 1 and self.choice_alim != 0:
            self.display_aliment()


    def display_save(self):
        self.db.connect_with_user(user_acc="StudentOF", passw="1Ksable$", db="openfoodfact")
        self.db.mycursor.execute("SELECT product_name FROM product WHERE save_product =1 ")
        myresult = self.db.mycursor.fetchall()
        self.choice_list(myresult)

    def substitute(self, categ_susbtitute, id_substitute, name_product):
            myresult = []
            self.list_aliment[:] = []
            while myresult == []:
                cat_modif = categ_susbtitute
                sql_substitute = "SELECT product_name FROM product WHERE Categories = %s AND id <> %s AND product_name <> %s LIMIT 1"
                val_substitute = (cat_modif, id_substitute, name_product)
                self.db.mycursor.execute(sql_substitute, val_substitute)
                myresult = self.db.mycursor.fetchall()
                nb = 0
                if len(myresult) == 0 and nb <= 10:
                    list_substitute = cat_modif.split(", ")
                    del list_substitute[-1]
                    cat_modif = ", ".join(list_substitute)
                    sql_substitute = "SELECT product_name FROM product WHERE Categories = %s AND id <> %s AND product_name <> %s LIMIT 1"
                    val_substitute = (cat_modif, id_substitute, name_product)
                    self.db.mycursor.execute(sql_substitute, val_substitute)
                    myresult = self.db.mycursor.fetchall()
                    nb +=1
                if len(myresult) != 0:
                    print("voici une liste des aliments substitué")
                    for x in myresult:
                        self.list_aliment.append(x)
                        self.choice_alim = 0
                    self.display_aliment()
                elif nb > 10:
                        print("nous n'avons pas trouvé d'aliment substitué")
