import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import numpy as np
import streamlit_option_menu
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import time
import importlib
from pages import login

load_dotenv(dotenv_path=".env.local")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login.login()
else:
    with st.sidebar:
        selected = option_menu(
            menu_title = "Menu Principal",
            options = ["Inicio","Recomendaciones","Escanear","Prescripciones"],
            icons = ["house","activity","receipt"],
            menu_icon = "cast",
        )
        
        st.markdown(
            """
            <style>
            .logout-button {
                position: fixed;
                left: 1rem;
                bottom: 1rem;
                z-index: 999999;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Cerrar Sesión", key="logout_button", help="Cerrar sesión actual", type="primary"):
            login.logout()
            st.rerun()

    def load_page(page):
        module = importlib.import_module(f"pages.{page}")
        module.run() 
        
    if selected == "Escanear":
        load_page('escanear')
    elif selected == "Recomendaciones":
        load_page('recomendaciones')
    elif selected == "Prescripciones":
        load_page('prescripciones')
    else:
        load_page('inicio')