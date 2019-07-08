#! /usr/bin/env python
# coding: utf-8
""" we find here all the constants that we will need.
INDEX OF CATEGORIE for the methode display aliment """

categ = """choisir votre catégorie : \n
                                    1 - Légumes \n
                                    2 - Viandes \n
                                    3 - Poissons \n
                                    4 - Biscuit et gateaux \n
                                    5 - Sandwich \n
                                    6 - Fromage \n
                                    7 - Chocolats \n
                                    8 - Boissons \n
                                    9 - Fruits \n
                                    0 - Quitter \n
                                    >>>"""



# DICT FOR CATEGORIE for the method in the file function for display list of aliments
categories = {
    "1": "Légumes",
    "2": "Viandes",
    "3": "Poissons",
    "4": "Biscuit",
    "5": "Sandwich",
    "6": "Fromage",
    "7": "Chocolats",
    "8": "Boissons",
    "9": "Fruits",
    "0": "Quitter"
    }

# Constant for input to display aliment

input_to_aliment = """                    1 - trouvez un substitut \n
                    2 - sauvegarder cet aliment dans les favoris \n
                    3 - revenir au menu \n
                    4 - retirer l'aliment des favoris\n"""


# FORMAT FOR DISPLAY ALIMENT in final function
format_aliment = """\n                    Nom du produit : {}\n
                    Lien url : {} \n
                    Catégories : {} \n
                    Score nutritionnel : {} \n
                    Magasins où le produit est en vente : {} \n"""
