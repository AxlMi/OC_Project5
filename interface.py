#! /usr/bin/env python
# coding: utf-8
import mysql.connector
from constant import *
from create_database import *
import os
import sys


class Menu:
    def __init__(self):
        self.db = Database()
        self.list_aliment = []
        self.choice = ""
        self.choice_categorie = ""
        self.choice_alim = ""
        self.last_choice = ""
        self.connect = self.db.connect_with_user(
                                user_acc="StudentOF",
                                passw="1Ksable$",
                                db="openfoodfact")

    # clear menu , use cls for nt and clear for other
    def clear_menu(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    # Method for the first menu interface
    def select_choice(self):
        self.choice = ""
        while self.choice is "":
            self.choice = input("            1 - Quel aliment souhaitez-vous remplacer ?\n\
            2 - Retrouver mes aliments substitués. \n\
            0 - quitter le programme\n>>> ")
            try:
                self.choice = int(self.choice)
            except ValueError:
                print("vous n'avez pas un nombre correspondant")
                self.choice = ""
            self.clear_menu()
            if self.choice == 1:
                self.select_categorie()
            elif self.choice == 2:
                self.display_save()
            elif self.choice == 0:
                sys.exit()
            else:
                print("entrez un nombre correspondant")
                self.select_choice()

    # method for select one categorie in the list " categ" in the constant file
    def select_categorie(self):
        self.choice_categorie = ""
        while self.choice_categorie is "":
            self.choice_categorie = input(categ)
            try:
                self.choice_categorie = int(self.choice_categorie)
            except ValueError:
                print("vous n'avez pas entrez un nombre correspondant")
                self.choice_categorie = ""
        self.clear_menu()
        if self.choice_categorie == 0:
            self.select_choice()
        elif self.choice_categorie in range(1, 10):
            self.display_list()
        else:
            print("vous n'avez pas entré un nombre correspondant")
            self.select_categorie()

    # this method will display the downloaded list of categ selectioned
    def display_list(self,):
        self.choice_alim = ""
        while self.choice_alim is "":
            self.db.mycursor.execute(
                "SELECT product.product_name FROM product\
                INNER JOIN categories\
                ON product.categories_id = categories.id\
                WHERE categories.categories LIKE %s ORDER BY RAND() LIMIT 8",
                (categories[str(self.choice_categorie)] + "%",))
            my_result = self.db.mycursor.fetchall()
            self.choice_list(my_result)

    """ We display the products of the desired category,
        we select the number and we add the choice
        to the variable choice_alim """
    def choice_list(self, result):
        self.list_aliment = ["Quitter", "Autres"]
        self.choice_alim = ""
        print("Voici une liste de votre catégorie : \n\
              \n 0 : Quitter\n\n1 : Autres\n")
        aliment_nb = 2
        if len(result) == 0:
            print("""Nous n'avons pas trouvé d'aliment correspondant à votre recherche""")
        else:
            for x in result:
                self.list_aliment.append(x)
                print(aliment_nb, ":", x, "\n")
                aliment_nb += 1
        try:
            self.choice_alim = int(input("Entrez le choix souhaité : >>> "))
        except ValueError:
            print("entrez un nombre valide")
            self.select_alim = ""
            self.choice_list(result)
        self.clear_menu()
        if self.choice_alim == 0:
            self.select_choice()
        elif self.choice_alim == 1:
            self.list_other_aliment()
        elif self.choice_alim in range(2, len(self.list_aliment)):
            self.display_aliment()
        else:
            print("entrez un nombre valide")
            self.choice_list(result)

    """We recover the choice of the list,
       we carry out a sql search and we display it"""
    def display_aliment(self,):
        sql = "SELECT product.*, categories.Categories, stores.store FROM product\
            INNER JOIN categories\
            ON categories.id = product.Categories_id\
            INNER JOIN stores\
            ON stores.id = product.stores_id\
            WHERE product_name = %s LIMIT 1"
        var = (self.list_aliment[self.choice_alim])
        self.db.mycursor.execute(sql, var,)
        myresult = self.db.mycursor.fetchall()
        for x in myresult:
            """ 1 for product name, 6 for URL,
                2 for categories, 3 for nutriscore and 4 for brands"""
            print(format_aliment.format(x[1], x[6], x[8], x[3], x[9]))
            try:
                self.last_choice = int(input(input_to_aliment))
            except ValueError:
                print("Entrez un nombre valide")
                self.last_choice = ""
                self.display_aliment()
            # depending on the choice, we display a substitute
            if self.last_choice == 1:
                self.substitute(x[8], x[0], x[1], x[3])
            # depending on the choice, add or remove favorites
            elif self.last_choice == 2:
                self.modify_save(x[0], 1)
            elif self.last_choice == 4:
                self.modify_save(x[0], 0)
            elif self.last_choice == 3:
                self.select_choice()
                break
            else:
                print("entrez un nombre correspondant")
        

    def modify_save(self, product, favorites):
        sql_update = """UPDATE product SET save_product = %s WHERE id = %s"""
        val_update = (favorites, product,)
        self.db.mycursor.execute(sql_update, val_update)
        self.db.mydb.commit()
        if favorites == 1:
            print("votre produit a été ajouté aux favoris")
        else:
            print("votre produit a été retiré des favoris")
        self.display_save()

    def list_other_aliment(self,):
        self.list_aliment[:] = []  # because maybe used by other method
        try:
            name_aliment = str(input("quel aliment recherchez vous ?"))
        except ValueError:
            print("entrez un mot valide")
            name_aliment = ""
            self.list_other_aliment()
        self.clear_menu()
        # we research one aliment by name of research
        self.db.mycursor.execute("SELECT product_name\
            FROM product\
            WHERE product_name\
            LIKE %s LIMIT 10", ("%"+name_aliment+"%",))
        my_result = self.db.mycursor.fetchall()
        self.choice_list(my_result)
        if self.choice_alim != 1 and self.choice_alim != 0:
            self.display_aliment()

    def display_save(self):
        self.db.mycursor.execute("SELECT product_name\
            FROM product WHERE save_product =1 ")
        myresult = self.db.mycursor.fetchall()
        self.choice_list(myresult)

    def research_sql_substitute(self,
                                cat_modif,
                                id_substitute,
                                name_product,
                                nutriscore_product):
        """we search with a similar category but with a name
        and a different id and we take the best nutritiong_grade"""
        sql_substitute = "SELECT product_name, Nutrition_grade\
        FROM product INNER JOIN categories\
        ON product.Categories_id = categories.id\
        WHERE categories.Categories LIKE %s\
        AND product.id != %s AND product.product_name != %s\
        ORDER BY Nutrition_grade ASC LIMIT 1"
        val_substitute = ("%"+cat_modif+"%", id_substitute, name_product)
        self.db.mycursor.execute(sql_substitute, val_substitute)
        return self.db.mycursor.fetchone()

    def substitute(self,
                   categ_susbtitute,
                   id_substitute,
                   name_product,
                   nutriscore_product):
        end_substitute = 1
        myresult = None
        self.list_aliment[:] = []
        self.choice_alim = ""
        """ as myresult that will become equal to my cursor is equal
        to nothing, we do not stop the loop"""
        while end_substitute:
            nb = 1
            cat_modif = categ_susbtitute
            print(cat_modif)
            if cat_modif == "":
                print("nous n'avons pas trouvé de meilleur aliment substitué")
                end_substitute = 0
                self.select_choice()
            elif myresult is None or myresult[1] > nutriscore_product:
                list_substitute = cat_modif.split(", ")
                del list_substitute[-nb:]
                categ_susbtitute = ", ".join(list_substitute)
                nb += 1
                myresult = self.research_sql_substitute(cat_modif,
                                                    id_substitute,
                                                    name_product,
                                                    nutriscore_product)
            # if we have one result , ok we can display our aliment
            elif myresult[1]<= nutriscore_product:
                print("voici un aliment substitué : ")
                self.list_aliment.append(myresult[:-1])
                self.choice_alim = 0
                self.display_aliment()
                break


menu = Menu()
menu.select_choice()
