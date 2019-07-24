CREATE USER 'StudentOF'@'localhost' IDENTIFIED BY '1Ksable$';

GRANT ALL PRIVILEGES ON * . * to 'StudentOF'@'localhost';

CREATE DATABASE IF NOT EXISTS openfoodfact;

CREATE TABLE IF NOT EXISTS brands (
            id INT AUTO_INCREMENT,
            brands VARCHAR(255) UNIQUE,
            PRIMARY KEY (id)
            )
            ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS stores (
            id INT AUTO_INCREMENT,
            store VARCHAR(255) UNIQUE,
            PRIMARY KEY (id)
            )
            ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT,
            Categories VARCHAR(255) UNIQUE,
            PRIMARY KEY (id)
            )
            ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS product (
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
            ENGINE=INNODB;