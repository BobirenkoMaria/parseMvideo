import sqlite3


def CREATE_TABLE():
    db = sqlite3.connect('marketplace_bot.db')

    cursor = db.cursor()
    cursor.execute("""CREATE TABLE laptops (
        id INTEGER,
        picture TEXT,
        name TEXT,
        price INTEGER,
        specifications TEXT,
        more TEXT   
    )""")

    db.commit()
    db.close()


def ALTER_COLUMN():
    db = sqlite3.connect('marketplace_bot.db')
    cursor = db.cursor()

    cursor.execute(f"""ALTER TABLE laptops ADD more TEXT""")

    db.commit()
    db.close()


def INSERT_NEW_LAPTOP(id_laptop, picture, name, price, specifics, more):
    db = sqlite3.connect('marketplace_bot.db')
    cursor = db.cursor()

    cursor.execute("""INSERT INTO laptops(id, picture, name, price, specifications, more)
        VALUES (?, ?, ?, ?, ?, ?)""", (id_laptop, picture, name, price, specifics, more))

    db.commit()
    db.close()
