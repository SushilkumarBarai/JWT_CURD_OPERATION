
from db import get_db


def insert_product(productname, companyname, rate):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO products(productname, companyname, rate) VALUES (?, ?, ?)"
    cursor.execute(statement, [productname, companyname, rate])
    db.commit()
    return True


def update_product(id, productname, companyname, rate):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE products SET productname = ?, companyname = ?, rate = ? WHERE id = ?"
    cursor.execute(statement, [productname, companyname, rate, id])
    db.commit()
    return True


def delete_product(id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM products WHERE id = ?"
    cursor.execute(statement, [id])
    db.commit()
    return True


def get_by_id(id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, productname, companyname, rate,mfgdate FROM products WHERE id = ?"
    cursor.execute(statement, [id])
    return cursor.fetchone()


def get_products():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, productname, companyname, rate, mfgdate FROM products"
    cursor.execute(query)
    return cursor.fetchall()
