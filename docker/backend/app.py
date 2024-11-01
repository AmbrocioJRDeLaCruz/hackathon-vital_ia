from flask import Flask, request, jsonify, Blueprint
from receipt import detect_data
from db.database_manager import DatabaseManager
from functions.bill_analyzer import process_bill
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")
app = Flask(__name__)
host = os.environ["AZURE_SQL_ENDPOINT"]
database = os.environ["AZURE_SQL_DB"]
db_username = os.environ["AZURE_SQL_USER"]
db_password = os.environ["AZURE_SQL_PASS"]

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400
    
    try:
        with DatabaseManager(host, database, db_username, db_password) as db_manager:
            query = """
            SELECT IdUsuario, Correo, Clave 
            FROM Usuario 
            WHERE Correo = ?
            """
            user = db_manager.fetch_one(query, (email,))
            
            if user and user['Clave'] == password:  # Aquí deberías usar hash en producción
                return jsonify({
                    "message": "Login exitoso",
                    "user_id": user['IdUsuario']
                }), 200
            else:
                return jsonify({"error": "Email o contraseña inválidos"}), 401
                
    except Exception as e:
        app.logger.error(f"Error en login: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/create_account", methods=["POST"])
def create_account():
    data = request.json
    required_fields = ["username", "password", "lastname", "email"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    # Validar longitud de campos
    if len(data['username']) < 2:
        return jsonify({"error": "El nombre debe tener al menos 2 caracteres"}), 400
    if len(data['password']) < 6:
        return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400
    if len(data['lastname']) < 2:
        return jsonify({"error": "El apellido debe tener al menos 2 caracteres"}), 400
    
    try:
        with DatabaseManager(host, database, db_username, db_password) as db_manager:
            success = db_manager.create_user(
                username=data['username'],
                password=data['password'],
                lastname=data['lastname'],
                email=data['email'],
                phone=data.get('phone', '')
            )
            
            if success:
                return jsonify({"message": "Usuario creado exitosamente"}), 201
            else:
                return jsonify({"error": "Error al crear el usuario"}), 500
                
    except Exception as e:
        app.logger.error(f"Error en create_account: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/image", methods=["POST"])
def image():
    if "file" in request.files:
        try:
            request_data = request.form.to_dict()            
            file = request.files["file"]
            file_content = file.read()
            products = detect_data(file_content)            
            process_bill(products, int(request_data["userId"]))
            return jsonify({"products": products}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        app.logger.warning("No se recibió ningun archivo")
        return jsonify({"error": "No file provided"}), 400

from invoice_routes import invoice_bp
app.register_blueprint(invoice_bp)

from precedent_routes import precedent_bp
app.register_blueprint(precedent_bp)

from recommendation_routes import recomendation_bp
app.register_blueprint(recomendation_bp)

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)