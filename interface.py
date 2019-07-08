#! /usr/bin/env python
# coding: utf-8
import mysql.connector
from Constant import *
from Create_database import *
from function import *

menu = Menu()
    
def interface():
    while menu.choice != 0:
        menu.select_choice()
        if menu.choice == 1:
            menu.select_categorie()
            if menu.choice_categorie != 0:
                menu.display_list()
                if menu.choice_alim == 0:
                    menu.choice
                elif menu.choice_alim == 1:
                    menu.list_other_aliment()
                else:
                    menu.display_aliment()
                    if menu.last_choice == 1:
                        pass
                    if menu.last_choice == 3:
                        menu.display_list
                menu.list_aliment[:] = [] # remove all list aliment
            menu.choice_categorie = None
            menu.choice_alim = None
            menu.choice = None
        elif menu.choice == 2:
            menu.display_save()
        if menu.choice_alim == 0:
            menu.choice = None
        elif menu.choice_alim == 1:
            menu.list_other_aliment()
        else:
            if menu.choice_alim is not None:
                menu.display_aliment()
                if menu.last_choice == 1:
                    pass # trouver substitut
                if menu.last_choice == 3:
                    menu.display_list
        menu.list_aliment[:] = [] # remove all list aliment
        menu.choice_categorie = None
        menu.choice_alim = None      

interface()



