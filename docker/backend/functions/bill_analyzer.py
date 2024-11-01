from dotenv import load_dotenv
from db.database_manager import DatabaseManager
from datetime import datetime
from categories import identify
import os

load_dotenv(dotenv_path=".env.local")

host = os.environ["AZURE_SQL_ENDPOINT"]
database = os.environ["AZURE_SQL_DB"]
username = os.environ["AZURE_SQL_USER"]
password = os.environ["AZURE_SQL_PASS"]

def process_bill(list, user_id: int):
    data = identify(list)
    __register_bill(data, user_id)

def __register_bill(list, user_id: int): 
    with DatabaseManager(host, database, username, password) as db_manager:
        inserted_id = db_manager.insert_data("Boleta", ["FechaBoleta", "IdUsuario"], [(datetime.now(), user_id)], "IdBoleta")
        tuples_list = [(item["name"], item["quantity"], item["category"], item["price"] , inserted_id) for item in list]
        db_manager.insert_data("Productos", ["Nombre", "Cantidad", "Categoria", "Costo", "IdBoleta"], tuples_list)