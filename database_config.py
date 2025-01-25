import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",           # Replace with your database host
        user="your_username",       # Replace with your database username
        password="your_password",   # Replace with your database password
        database="empower_women"    # Replace with your database name
    )
    return connection
