#! /usr/bin/env python
# coding: utf-8


#INDEX OF CATEGORIE
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



# DICT FOR CATEGORIE
categories = {
    "1" : "Légumes" ,
    "2" : "Viandes",
    "3" : "Poissons",
    "4" : "Biscuit",
    "5" : "Sandwich",
    "6" : "Fromage",
    "7" : "Chocolats",
    "8" : "Boissons",
    "9" : "Fruits",
    "0" : "Quitter"
    }

# FORMAT FOR DISPLAY ALIMENT

format_aliment = """Nom du produit : {} 
                    Lien url : {} \n
                    Catégories : {} \n
                    Score nutritionnel : {} \n
                    Magasins où le produit est en vente : {} \n
            """

