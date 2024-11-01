from datetime import datetime
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from db.database_manager import DatabaseManager
import os

recomendation_bp = Blueprint('recomendation', __name__)
load_dotenv(dotenv_path=".env.local")
host = os.environ["AZURE_SQL_ENDPOINT"]
database = os.environ["AZURE_SQL_DB"]
username = os.environ["AZURE_SQL_USER"]
password = os.environ["AZURE_SQL_PASS"]

@recomendation_bp.route('/api/recommendations', methods=['GET'])
def get_recomendaciones():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({"error": "userId is required"}), 400
    
    try:
        db_manager = DatabaseManager(host, database, username, password)
        db_manager.connect()
        recommendations = {}
        query = """
        SELECT Detalle
            FROM RecAlimentarias
            WHERE IdUsuario = ?
        """
        recommendations['dietary'] = db_manager.fetch_all(query, (user_id,))
        
        query = """
        SELECT Detalle
            FROM RecEnfermedades
            WHERE IdUsuario = ?
        """
        recommendations['diseases'] = db_manager.fetch_all(query, (user_id,))
        return jsonify({"recommendations": recommendations}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
