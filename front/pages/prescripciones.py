import streamlit as st
import requests
import ast
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")
api_server = os.environ["API_SERVER"]
port = os.environ["PORT"]

def run():
    st.title("Prescripciones")
    user_id = st.session_state.get('user_id', 1)

    prescripcion_input = st.text_input("Ingresa alguna prescripción o malestar para generar recomendaciones perfectas para ti.")
    if st.button("Guardar"):
        api_url = f"http://{api_server}:{port}/api/prescedente"
        if prescripcion_input:
            try:
                response = requests.post(api_url, json={"userId": user_id, "precedent": prescripcion_input})
                response.raise_for_status()
                st.success("Registro ingresado!")

            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Introduzca un texto antes de guardar.")

    try:
        response = requests.get(f"http://{api_server}:{port}/api/prescedentes?userId={user_id}")
        response.raise_for_status()
        if response.status_code == 200:
            precedentes = response.json().get("precedentes", [])
            if not precedentes:
                st.info("Sin prescedentes registrados.")
            else:
                # for precedente in ast.literal_eval(precedentes):
                for precedente in precedentes:
                    st.write(precedente.get("Detalle",""))
                    st.write("---")
                   
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return
