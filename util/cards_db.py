import sqlite3

#Setup
DB_FILE = "data/cards.db"

def user_exists(id):
    '''Checks if a user exists'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT * FROM users WHERE id = ?;"
    c.execute(command,(id,))
    account = c.fetchall()
    has_account = account != []
    db.close()
    return has_account

def add_user(id):
    '''Adds a user'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO users (id,balance) VALUES (?,50);"
    c.execute(command,(id,))
    db.commit()
    db.close()


def get_balance(id):
    '''Gets the balance of the user'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT balance FROM users WHERE id = ?;"
    c.execute(command,(id,))
    balance = c.fetchall()
    db.close()
    return balance[0][0]

def update_balance(id, val):
    '''Updates the balance of the user to val'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "UPDATE users SET balance=? WHERE id=?"
    c.execute(command, (val, id))
    db.commit()
    db.close()

def get_cards(id):
    '''Gets the cards that the user has'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT card_id FROM cards WHERE id = ?;"
    c.execute(command,(id,))
    cards = c.fetchall()
    db.close()

    return [i[0] for i in cards] #Flatten the list of tuples

def add_cards(id, items):
    '''Adds the new cards for the user'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO cards (id,card_id) VALUES (?,?);"
    for item in items:
        c.execute(command, (id, item))
    db.commit()
    db.close()

def remove_card(id,card_id):
    '''Removes a card from the user'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #Counts the number of the card the user has
    command = "SELECT * FROM cards WHERE id = ? AND card_id = ?;"
    c.execute(command,(id,card_id))

    count = len(c.fetchall())

    #Remove all the cards
    command = "DELETE FROM cards WHERE id = ? AND card_id = ?;"
    c.execute(command,(id,card_id))
    db.commit()
    db.close()

    #Add back n-1 of those cards
    add_cards(id, [card_id] * (count - 1))































# MAKE TABLES AND DATABASE IF THEY DONT EXIST
db = sqlite3.connect(DB_FILE)
c = db.cursor()
commands = []
commands += ["CREATE TABLE IF NOT EXISTS users(id TEXT, balance INTEGER)"]
commands += ["CREATE TABLE IF NOT EXISTS cards(id TEXT, card_id INTEGER)"]
for command in commands:
    c.execute(command)
db.commit()
c.close()
