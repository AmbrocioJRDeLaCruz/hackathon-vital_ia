import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")
api_server = os.environ["API_SERVER"]
port = os.environ["PORT"]

def init_session_state():
    try:
        saved_session = st.session_state.get('_saved_session', {})
        if saved_session:
            st.session_state.update(saved_session)
    except Exception:
        pass

def save_session_state():
    session_data = {
        'logged_in': st.session_state.get('logged_in', False),
        'email': st.session_state.get('email', ''),
        'user_id': st.session_state.get('user_id', None)
    }
    st.session_state['_saved_session'] = session_data

def login():
    init_session_state()
    
    if "form_key" not in st.session_state:
        st.session_state.form_key = 0
    
    if "form_state" not in st.session_state:
        st.session_state.form_state = "login"
    
    if st.session_state.form_state == "login":
        with st.container():
            st.title("Login")
            form_key = f"login_form_{st.session_state.form_key}"
            with st.form(key=form_key):
                email = st.text_input("Email")
                password = st.text_input("Contraseña", type="password")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    submit = st.form_submit_button("Login")
                    if submit:
                        if not email or not password:
                            st.error("Por favor complete todos los campos")
                            return
                            
                        response = requests.post(f"{api_server}:{port}/login", 
                                              json={"email": email, "password": password})
                        if response.status_code == 200:
                            st.session_state.update({
                                "logged_in": True,
                                "email": email,
                                "user_id": response.json().get("user_id", 1)
                            })
                            save_session_state()
                            st.success("¡Inicio de sesión exitoso!")
                            st.rerun()
                        else:
                            st.error("Email o contraseña inválidos")
                            st.session_state.form_key += 1
                
                with col2:
                    if st.form_submit_button("Crear Cuenta"):
                        st.session_state.form_state = "create_account"
                        st.rerun()
    else:
        with st.container():
            st.title("Crear Cuenta")
            form_key = f"create_account_form_{st.session_state.form_key}"
            with st.form(key=form_key):
                new_username = st.text_input("Usuario")
                new_password = st.text_input("Contraseña", type="password")
                new_lastname = st.text_input("Apellido")
                new_email = st.text_input("Email")
                new_phone = st.text_input("Teléfono")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("Crear"):
                        if not all([new_username, new_password, new_lastname, new_email]):
                            st.error("Por favor complete todos los campos requeridos")
                            return
                            
                        # Validar formato de email
                        if '@' not in new_email or '.' not in new_email:
                            st.error("Por favor ingrese un email válido")
                            return
                            
                        # Validar longitud de contraseña
                        if len(new_password) < 6:
                            st.error("La contraseña debe tener al menos 6 caracteres")
                            return
                            
                        create_response = requests.post(f"{api_server}:{port}/create_account", 
                            json={
                                "username": new_username,
                                "password": new_password,
                                "lastname": new_lastname,
                                "email": new_email,
                                "phone": new_phone
                            })
                        if create_response.status_code == 201:
                            st.success("¡Cuenta creada exitosamente!")
                            st.session_state.form_state = "login"
                            st.rerun()
                        else:
                            error_msg = create_response.json().get("error", "Error desconocido")
                            st.error(f"Error al crear la cuenta: {error_msg}")
                
                with col2:
                    if st.form_submit_button("Volver al Login"):
                        st.session_state.form_state = "login"
                        st.rerun()

def logout():
    for key in ["logged_in", "email", "user_id", "form_state", "form_key", "_saved_session"]:
        if key in st.session_state:
            del st.session_state[key]