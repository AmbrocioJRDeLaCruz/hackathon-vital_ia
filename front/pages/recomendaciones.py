import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")
api_server = os.environ["API_SERVER"]
port = os.environ["PORT"]

def recommendations():
    user_id = st.session_state.get('user_id', 1)
    try:
        response = requests.get(f"http://{api_server}:{port}/api/recommendations?userId={user_id}")
        response.raise_for_status()
        if response.status_code == 200:
            dietaries = response.json().get("recommendations").get("dietary", [])
            diseases = response.json().get("recommendations").get("diseases", [])
            return dietaries,diseases
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return
    
def run():
    st.title("Recomendaciones")
    tab1, tab2 = st.tabs(["Dietéticas", "De salud"])
    dietaries, diseases = recommendations()
    with tab1:
        if not dietaries:
            st.info("No tenemos recomendaciones alimentarias de momento.")
        else:
            for dietary in dietaries:
                st.write(dietary.get("Detalle",""))
                st.write("---")                        
    with tab2:
        if not diseases:
            st.info("No tenemos recomendaciones de enfermedades de momento.")
        else:
            for disease in diseases:
                st.write(disease.get("Detalle",""))
                st.write("---")