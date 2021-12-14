from peewee import MySQLDatabase

DATABASE_NAME = "CRM"
USER = "root"
PASSWORD = "35739517"
HOST = "192.168.0.51"
PORT = 3307

connection = MySQLDatabase(DATABASE_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)