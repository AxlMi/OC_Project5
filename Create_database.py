#! /usr/bin/env python
# coding: utf-8
import mysql.connector


""" This script will connect to mysql and create : a user, an database ,
 an table of data to fill whit the API of openfoodfact"""


class Database:
    """this function will connect the user to the database"""
    def connect_with_user(self, user_acc, passw, db):
        try:
            self.mydb = mysql.connector.connect(
                                                host="localhost",
                                                user=user_acc,
                                                passwd=passw,
                                                database=db,)
            self.mycursor = self.mydb.cursor()
        except mysql.connector.errors.ProgrammingError:
            print("votre nom d'utilisateur ou mot de passe est incorrect")
        except Exception as e:
            print("[ERREUR : ]", e)
            self.mycursor.close()
            self.mydb.close()

    """ to create a user with creation and modification rights"""

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

    def create_db(self,):
        self.mycursor = self.mydb.cursor()
        data_name = 'CREATE DATABASE IF NOT EXISTS openfoodfact;'
        self.mycursor.execute(data_name)
        print("Création de la base de données")

    def create_table(self,):
        table_cat_product = """CREATE TABLE IF NOT EXISTS cat_product (
            id INT AUTO_INCREMENT,
            Categories VARCHAR(255) UNIQUE,
            PRIMARY KEY (id)
            )
            ENGINE=INNODB;"""
        self.mycursor.execute(table_cat_product)
        print('la table cat_product a été crée')

        table_product = """CREATE TABLE IF NOT EXISTS product (
            id INT AUTO_INCREMENT,
            Product_name TINYTEXT NOT NULL,
            Categories_id INT DEFAULT 0 NOT NULL,
            Nutrition_grade VARCHAR(5) NOT NULL,
            Brands TINYTEXT,
            Stores TEXT,
            url_product TEXT,
            save_product TINYINT(1),
            PRIMARY KEY (id),
            CONSTRAINT fk_numero_categorie\
            FOREIGN KEY(Categories_id)\
            REFERENCES cat_product(id)
            )
            ENGINE=INNODB;"""
        self.mycursor.execute(table_product)
        print('la table Product a été crée')


# main function to know the information of the user
def main():
    DB = Database()
    DB.connect_with_user(input('entrez votre nom d\'utilisateur mysql : '),
                         input('entrez votre MDP : '), '')
    DB.create_user()
    DB.connect_with_user('StudentOF', '1Ksable$', '')
    DB.create_db()
    DB.connect_with_user('StudentOF', '1Ksable$', 'openfoodfact')
    DB.create_table()
    print("fermeture de la base de données")
    DB.mycursor.close()
    DB.mydb.close()


if __name__ == "__main__":
    main()
