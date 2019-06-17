#! /usr/bin/env python
# coding: utf-8
import mysql.connector
from DB import Database

class Menu:


    def select_choice(self):
        self.choice = None
        while self.choice is None:
            self.choice = input("1- Quel aliment souhaitez-vous remplacer ?\n2 - Retrouver mes aliments substitués. ")
            try:
                self.choice = int(self.choice)
            except:
                print("vous n'avez pas entrez une valeur correspondante")
                self.choice = None
        return self.choice


    def select_categorie(self):
        self.choice_categorie = None
        while self.choice_categorie is None:
            self.choice_categorie = input("""choisir votre catégorie : \n
                                    1 - Fruits et légumes \n
                                    2 - Viandes \n
                                    3 - Poissons \n
                                    4 - Biscuit et gateaux \n
                                    5 - Sandwich \n
                                    6 - Produit laitiers \n
                                    7 - Fromage \n
                                    8 - Chocolats \n
                                    9 - Boissons \n
                                    0 - Autres \n""")
            try:
                self.choice_categorie = int(self.choice_categorie)
            except:
                print("vous n'avez pas entrez une valeur correspondante")
                self.choice_categorie = None
        return self.choice_categorie

        

    

test = Menu()
test.select_categorie()