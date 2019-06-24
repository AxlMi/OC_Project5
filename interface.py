#! /usr/bin/env python
# coding: utf-8
import mysql.connector
from Constant import *
from Create_database import *
from function import *

menu = Menu()

def function_interface():
    if menu.choice_categorie != 0:
        menu.display_list()
        if menu.choice_alim == 0:
            menu.choice_categorie
        elif menu.choice_alim == 1:
            pass # faire l'alternative autres
        else:
            menu.display_aliment()
            if menu.last_choice == 1:
                pass # trouver substitut
            if menu.last_choice == 2:
                pass #save aliment
            if menu.last_choice == 3:
                menu.display_list
        menu.list_aliment[:] = [] # remove all list aliment
    menu.choice_categorie = None
    menu.choice_alim = None
    menu.choice = None
    
def interface():
    while menu.choice != 0:
        menu.select_choice()
        if menu.choice == 1:
            menu.select_categorie()
            function_interface()
        elif menu.choice == 2:
            menu.display_save() #retrouver aliments substitués
            function_interface()           

interface()



