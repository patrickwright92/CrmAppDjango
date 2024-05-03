import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'GT1$3P7wdaB#2'
)

# Prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database

cursorObject.execute("CREATE DATABASE crmappdata")

print("All Done!")