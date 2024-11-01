from datetime import datetime
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from db.database_manager import DatabaseManager
import os

precedent_bp = Blueprint('precedent', __name__)
load_dotenv(dotenv_path=".env.local")
host = os.environ["AZURE_SQL_ENDPOINT"]
database = os.environ["AZURE_SQL_DB"]
username = os.environ["AZURE_SQL_USER"]
password = os.environ["AZURE_SQL_PASS"]

@precedent_bp.route('/api/prescedente', methods=['POST'])
def insert_prescedente():
    data = request.json
    
    try:
        db_manager = DatabaseManager(host, database, username, password)
        db_manager.connect()
        
        db_manager.insert_precedent(
            user_id=data.get('userId'),
            precedent=data.get('precedent'),
        )
        return jsonify({"message": "Precedente insertado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@precedent_bp.route('/api/prescedentes', methods=['GET'])
def get_prescendetes():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({"error": "userId is required"}), 400
    
    try:
        db_manager = DatabaseManager(host, database, username, password)
        db_manager.connect()
        
        query = """
        SELECT Detalle
            FROM RecPrecedentes
            WHERE IdUsuario = ?
        """
        precedentes = db_manager.fetch_all(query, (user_id,))
        return jsonify({"precedentes": precedentes}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
