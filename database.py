import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv as caricaenv

caricaenv()

configuratore={
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}






if __name__ == '__main__':
    pass