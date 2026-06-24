

CREATE DATABASE IF NOT EXISTS shopeasy;
USE shopeasy;

CREATE TABLE users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    phone       VARCHAR(20),
    password    VARCHAR(255) NOT NULL,
    address     VARCHAR(255),
    created_at  DATETIME,
    updated_at  DATETIME
);

CREATE TABLE categories (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    parent_id   INT,
    name        VARCHAR(100) NOT NULL,
    image       VARCHAR(255),
    description TEXT,
    created_at  DATETIME,
    updated_at  DATETIME,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

CREATE TABLE products (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    subcategory_id   INT NOT NULL,
    name             VARCHAR(150) NOT NULL,
    image            VARCHAR(255),
    price            DECIMAL(10,2) NOT NULL,
    stock            INT DEFAULT 0,
    discount_percent VARCHAR(10),
    description      TEXT,
    created_at       DATETIME,
    updated_at       DATETIME,
    FOREIGN KEY (subcategory_id) REFERENCES categories(id)
);
