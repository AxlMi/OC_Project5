#! /usr/bin/env python
# coding: utf-8
import mysql.connector


""" This script will connect to mysql and create : a user, an database ,
 an table of data to fill whit the API of openfoodfact"""


class Database:

    # this function will connect the user to the database
    def connect_with_user(self, user_acc, passw, db):
        try:
            self.mydb = mysql.connector.connect(
                connect_timeout=6000,
                host="localhost",
                user=user_acc,
                passwd=passw,
                database=db,)
            self.mycursor = self.mydb.cursor(buffered=True)
        except mysql.connector.errors.ProgrammingError:
            print("votre nom d'utilisateur ou mot de passe est incorrect")
        except Exception as except_error:
            print("[ERREUR : ]", except_error)
            self.mycursor.close()
            self.mydb.close()

    # to create a user with creation and modification rights
    def create_user(self,):
        try:
            # create 3 variables for create user allowed privilege and actualiz
            user = "CREATE USER 'StudentOF'@'localhost'\
                    IDENTIFIED BY '1Ksable$';"
            privilege = "GRANT ALL PRIVILEGES ON * . *\
                        to 'StudentOF'@'localhost';"
            flush = "FLUSH PRIVILEGES;"
            self.mycursor.execute(user)
            self.mycursor.execute(privilege)
            self.mycursor.execute(flush)
            print("Création de l'utilisateur")
        # if the user already exists we validate anyway
        except mysql.connector.errors.DatabaseError:
            print("Utilisateur déja existant")

    # to create database
    def create_db(self,):
        self.mycursor = self.mydb.cursor()
        data_name = 'CREATE DATABASE IF NOT EXISTS openfoodfact;'
        self.mycursor.execute(data_name)
        print("Création de la base de données")

    def create_table(self,):
        table_brands_product = """CREATE TABLE IF NOT EXISTS brands (
            id INT AUTO_INCREMENT,
            brands VARCHAR(255) UNIQUE,
            PRIMARY KEY (id)
            )
            ENGINE=INNODB;"""
        self.mycursor.execute(table_brands_product)
        print('la table brands a été crée')

        table_stores_product = """CREATE TABLE IF NOT EXISTS stores (
            id INT AUTO_INCREMENT,
            store VARCHAR(255) UNIQUE,
            PRIMARY KEY (id)
            )
            ENGINE=INNODB;"""
        self.mycursor.execute(table_stores_product)
        print('la table stores a été crée')

        table_cat_product = """CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT,
            Categories VARCHAR(255) UNIQUE,
            PRIMARY KEY (id)
            )
            ENGINE=INNODB;"""
        self.mycursor.execute(table_cat_product)
        print('la table categories a été crée')

        table_product = """CREATE TABLE IF NOT EXISTS product (
            id INT AUTO_INCREMENT,
            Product_name TINYTEXT NOT NULL,
            Categories_id INT DEFAULT 0 NOT NULL,
            Nutrition_grade VARCHAR(5) NOT NULL,
            Brands_id INT DEFAULT 0 NOT NULL,
            Stores_id INT DEFAULT 0 NOT NULL,
            url_product TEXT,
            save_product TINYINT(1),
            PRIMARY KEY (id),
            CONSTRAINT fk_numero_categorie\
            FOREIGN KEY(Categories_id)\
            REFERENCES categories(id),
            CONSTRAINT fk_numero_brands\
            FOREIGN KEY(Brands_id)\
            REFERENCES brands(id),\
            CONSTRAINT fk_numero_stores\
            FOREIGN KEY(Stores_id)\
            REFERENCES stores(id)\
            )
            ENGINE=INNODB;"""
        self.mycursor.execute(table_product)
        print('la table Product a été crée')

    def exit_db(self):
        if self.mycursor and self.mydb:
            self.mycursor.close()
            self.mydb.close()


# main function to know the information of the user
def main():
    dbase = Database()
    dbase.connect_with_user(input('entrez votre nom d\'utilisateur mysql : '),
                            input('entrez votre MDP : '), '')
    dbase.create_user()
    dbase.connect_with_user('StudentOF', '1Ksable$', '')
    dbase.create_db()
    dbase.connect_with_user('StudentOF', '1Ksable$', 'openfoodfact')
    dbase.create_table()
    print("fermeture de la base de données")
    dbase.exit_dbase()


if __name__ == "__main__":
    main()
