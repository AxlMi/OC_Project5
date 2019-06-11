#! /usr/bin/env python
# coding: utf-8
import mysql.connector


""" This script will connect to mysql and create : a user, an database ,
 an table of data to fill whit the API of openfoodfact"""

class Database:

    """ this function will connect the user to the database"""
    
    def connect_with_user(self, user_acc, passw, db):
        try:
            self.mydb = mysql.connector.connect(
            host="localhost",
            user=user_acc,
            passwd=passw,
            database=db,)
            self.mycursor = self.mydb.cursor()
            print('Connexion à {}'.format(user_acc))
        except mysql.connector.errors.ProgrammingError: 
            print("votre nom d'utilisateur ou mot de passe est incorrect")

    """ to create a user with creation and modification rights"""

    def create_user(self,):
        try:
            user = "CREATE USER 'StudentOF'@'localhost' IDENTIFIED BY '1Ksable$';"
            privilege = "GRANT ALL PRIVILEGES ON * . * to 'StudentOF'@'localhost';"
            flush = "FLUSH PRIVILEGES;"
            self.mycursor.execute(user)
            self.mycursor.execute(privilege)
            self.mycursor.execute(flush)
            print("Création de l'utilisateur")
        except mysql.connector.errors.DatabaseError: #if the user already exists we validate anyway
            print("creation de l'utilisateur")
    
    
    def create_db(self,):
        self.mycursor = self.mydb.cursor()
        data_name = 'CREATE DATABASE IF NOT EXISTS openfoodfact;'
        self.mycursor.execute(data_name)
        print("Création de la base de données")


    def create_table(self,):
        table_product = """CREATE TABLE IF NOT EXISTS product (
            id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
            Product_name TINYTEXT NOT NULL,
            Categories TEXT NOT NULL,
            Nutrition_grade VARCHAR(1),
            Brands TINYTEXT,
            Stores TINYTEXT,
            url_product TINYTEXT,
            PRIMARY KEY (id)
            )
            ENGINE=INNODB;"""
        self.mycursor.execute(table_product)
        print('la table Product a été crée')

def main():
    DB = Database()
    DB.connect_with_user(input('entrez votre nom d\'utilisateur mysql : '),
    input('entrez votre MDP : '), '')
    DB.create_user()
    DB.connect_with_user('StudentOF', '1Ksable$', 'openfoodfact')
    DB.create_db()
    DB.create_table()
    
main()