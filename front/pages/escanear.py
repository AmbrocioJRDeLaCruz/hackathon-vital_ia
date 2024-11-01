import time
import requests
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")
api_server = os.environ["API_SERVER"]
port = os.environ["PORT"]

def run():
    user_id = st.session_state.get('user_id', 1)
    
    st.title("Pagina Escanear")
    st.header(f"**Escanear tu boleta y cambiemos el mundo**")

    image_url = f"http://{api_server}:{port}/image"
    scan_invoice_url = f"http://{api_server}:{port}/scan_invoice"

    img_file_buffer = st.camera_input("")

    if img_file_buffer is not None:
        image_bytes = img_file_buffer.getvalue()
        files = {
            "file": ("photo.jpg", image_bytes, "image/jpeg")
        }
        data = {'userId': user_id}
        try:
            response = requests.post(image_url, files=files, data=data)
            
            if response.status_code == 200:
                products = response.json().get("products", [])
                
                if not products:
                    st.error("No se pudieron detectar productos en la imagen. Por favor, intente nuevamente.")
                    return
                
                st.subheader("Productos detectados:")
                for product in products:
                    with st.container():
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Nombre:** {product.get('name', 'No especificado')}")
                            st.write(f"**Categoría:** {product.get('category', 'No especificada')}")
                        with col2:
                            st.write(f"**Cantidad:** {product.get('quantity', 'No especificada')}")
                            st.write(f"**Precio:** ${product.get('cost', '0.00')}")
                        st.divider()
                
                invoice_data = {
                    "products": products,
                    "userId": user_id
                }
                invoice_response = requests.post(scan_invoice_url, json=invoice_data)
                
                if invoice_response.status_code == 201:
                    st.success("¡Productos guardados exitosamente! Puede verlos en la página de inicio.")
                else:
                    st.error(f"Error al guardar los productos: {invoice_response.json().get('error', 'Error desconocido')}")
            else:
                st.error(f"Error al procesar la imagen: {response.json().get('error', 'Error desconocido')}")
                
        except requests.exceptions.RequestException as e:
            st.error(f"Error de conexión: {str(e)}")
            return