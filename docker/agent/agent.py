import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from dev_agent_enfermedades import agent as agent_enfermedades
from dev_agent_alimentarias import agent as agent_alimentarias

import logging
import sys

load_dotenv(dotenv_path=".env.local")
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Stream logs to stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
app.logger.addHandler(stdout_handler)

# Stream errors to stderr
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
app.logger.addHandler(stderr_handler)

@app.route("/alimentarias", methods=["POST"])
def alimentarias():
    if request.is_json:
        data = request.get_json()
        id = data['id']
        edad = data['edad']
        try:
            agent_alimentarias(id, edad)
            response_data = {
                "message": "inicio de recomendaciones alimentarias"
            }
            status_code = 200
        except Exception as e:
            response_data = {
                "message": e
            }
            status_code = 500
            app.logger.error(f"Error: {e}")
        return jsonify(response_data), status_code
    else:
        # Handle missing data
        app.logger.info("No JSON data or file provided")
        return jsonify({"error": "No JSON data or file provided"}), 400
    
@app.route("/enfermedades", methods=["POST"])
def enfermedades():
    if request.is_json:
        data = request.get_json()
        id = data['id']
        edad = data['edad']
        try:
            agent_enfermedades(id, edad)
            response_data = {
                "message": "inicio de identificación de enfermedades"
            }
            status_code = 200
        except Exception as e:
            response_data = {
                "message": e
            }
            status_code = 500
            app.logger.error(f"Error: {e}")
        return jsonify(response_data), status_code
    else:
        # Handle missing data
        app.logger.info("No JSON data or file provided")
        return jsonify({"error": "No JSON data or file provided"}), 400
    
if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)