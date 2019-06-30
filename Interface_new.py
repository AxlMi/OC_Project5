#! /usr/bin/env python
# coding: utf-8
import mysql.connector
from Constant import *
from Create_database import *
from function import *




def main_interface():
    menu = Menu()
    end_interface = 1
    while end_interface:
        menu.select_choice()
        if menu.choice == 1:
            menu.select_categorie()
            if menu.choice_categorie == 0:
                continue
            else:
                menu.display_list()
                if menu.choice_alim == 0:
                    continue
                if menu.choice_alim == 1:
                    menu.list_other_aliment()
                else:
                    menu.display_aliment()
        elif menu.choice == 2:
            menu.display_save()
            if menu.choice_alim == 0:
                continue
            if menu.choice_alim == 1:
                menu.list_other_aliment()
                if menu.choice_alim == 0:
                    continue
                elif menu.choice_alim == 1:
                    menu.list_other_aliment()
            else:
                menu.display_aliment() 
        elif menu.choice == 0:
            break

main_interface()
        
    
