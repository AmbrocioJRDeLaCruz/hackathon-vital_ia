from datetime import datetime
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from db.database_manager import DatabaseManager
import os

invoice_bp = Blueprint('invoice', __name__)

load_dotenv(dotenv_path=".env.local")
host = os.environ["AZURE_SQL_ENDPOINT"]
database = os.environ["AZURE_SQL_DB"]
username = os.environ["AZURE_SQL_USER"]
password = os.environ["AZURE_SQL_PASS"]

@invoice_bp.route('/scan_invoice', methods=['POST'])
def scan_invoice():
    data = request.json
    try:
        db_manager = DatabaseManager(host, database, username, password)
        db_manager.connect()
        
        boleta_id = db_manager.insert_boleta(data['userId'])
        
        for product in data['products']:
            db_manager.insert_product(
                nombre=product['name'],
                cantidad=product.get('quantity'),
                categoria=product.get('category'),
                porcentaje_consumo=product.get('consumption_percentage'),
                fecha_vencimiento=product.get('expiry_date'),
                costo=product.get('cost'),
                id_boleta=boleta_id
            )
        return jsonify({"message": "Productos insertados correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@invoice_bp.route('/api/productos', methods=['GET'])
def get_productos():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({"error": "userId is required"}), 400
    
    try:
        db_manager = DatabaseManager(host, database, username, password)
        db_manager.connect()
        
        query = """
        SELECT p.Nombre, p.Cantidad, p.Categoria, 
               CONVERT(VARCHAR(10), p.FechaVencimiento, 23) as FechaVencimiento,
               p.PorcentajeConsumo, p.Costo
        FROM Productos p
        INNER JOIN Boleta b ON p.IdBoleta = b.IdBoleta
        WHERE b.IdBoleta = (
            SELECT TOP 1 IdBoleta 
            FROM Boleta 
            WHERE IdUsuario = ? 
            ORDER BY FechaBoleta DESC
        )
        """
        
        productos = db_manager.fetch_all(query, (user_id,))
        return jsonify({"productos": productos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
