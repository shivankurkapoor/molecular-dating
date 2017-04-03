from peewee import *

db = MySQLDatabase('dating',
                   user='root',
                   password='Roopak@1610')

def db_connect():
    db.connect()

def db_disconnect():
    db.close()
