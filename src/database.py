import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()

# Obtener las variables de entorno
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Conexión a la base de datos
database = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
