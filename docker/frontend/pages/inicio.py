import streamlit as st
import requests
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")
api_server = os.environ["API_SERVER"]
port = os.environ["PORT"]

def create_category_chart(productos):
    # Agrupar productos por categoría
    category_data = {}
    for producto in productos:
        categoria = producto.get('Categoria', 'Sin categoría')
        category_data[categoria] = category_data.get(categoria, 0) + 1
    
    #gráfico de pastel
    fig_category = {
        'data': [{
            'labels': list(category_data.keys()),
            'values': list(category_data.values()),
            'type': 'pie',
            'hole': .4,
        }],
        'layout': {
            'title': 'Distribución por Categorías',
            'showlegend': True
        }
    }
    return fig_category

def create_consumption_chart(productos):
    # Agrupar por categoría y calcular consumo promedio
    consumption_data = {}
    for producto in productos:
        categoria = producto.get('Categoria', 'Sin categoría')
        consumo = producto.get('PorcentajeConsumo')
        if consumo is None:
            consumo = 0
            
        if categoria not in consumption_data:
            consumption_data[categoria] = {'total': 0, 'count': 0}
        consumption_data[categoria]['total'] += consumo
        consumption_data[categoria]['count'] += 1
    
    # Calcular promedios
    categories = []
    averages = []
    for cat, data in consumption_data.items():
        categories.append(cat)
        averages.append(data['total'] / data['count'])
    
    # gráfico de barras
    fig_consumption = {
        'data': [{
            'x': categories,
            'y': averages,
            'type': 'bar',
            'name': 'Consumo Promedio'
        }],
        'layout': {
            'title': 'Porcentaje de Consumo Promedio por Categoría',
            'yaxis': {'title': 'Porcentaje'},
            'showlegend': False
        }
    }
    return fig_consumption

def create_cost_chart(productos):
    # Agrupar costos por categoría
    cost_data = {}
    for producto in productos:
        categoria = producto.get('Categoria', 'Sin categoría')
        costo = producto.get('Costo', 0)
        if categoria not in cost_data:
            cost_data[categoria] = 0
        cost_data[categoria] += costo
    
    #gráfico de barras
    fig_cost = {
        'data': [{
            'x': list(cost_data.keys()),
            'y': list(cost_data.values()),
            'type': 'bar',
            'name': 'Costo Total'
        }],
        'layout': {
            'title': 'Costo Total por Categoría',
            'yaxis': {'title': 'Costo ($)'},
            'showlegend': False
        }
    }
    return fig_cost

def run():
    st.title("Listado de productos")
    user_id = st.session_state.get('user_id', 1)
    new_products = st.session_state.get('new_products', False)

    try:
        response = requests.get(f"{api_server}:{port}/api/productos?userId={user_id}")
        if response.status_code == 200:
            productos = response.json().get("productos", [])
            if not productos:
                if new_products:
                    st.error("Error al cargar los productos recién escaneados.")
                else:
                    st.info("No hay productos registrados aún. Por favor, escanee una factura.")
                st.session_state['new_products'] = False
                return
            
            tab1, tab2 = st.tabs(["Lista", "Estadísticas"])
            
            with tab1:
                for idx, producto in enumerate(productos):
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        st.write(f"**{producto.get('Nombre', 'Sin nombre')}**")
                        categoria = producto.get('Categoria', 'Sin categoría')
                        st.write(f"Categoría: {categoria}")
                    
                    with col2:
                        fecha_venc = producto.get('FechaVencimiento')
                        if fecha_venc:
                            st.write(f"Vence: {fecha_venc}")
                        else:
                            st.write("Vence: No especificado")
                        
                        cantidad = producto.get('Cantidad', 'No especificada')
                        st.write(f"Cantidad: {cantidad}")
        
                        costo = producto.get('Costo', 0.0)
                        if costo is None:
                            st.write("Costo: No especificado")
                        else:
                            st.write(f"Costo: ${costo:.2f}")
                    
                    with col3:
                        porcentaje_actual = producto.get('PorcentajeConsumo', 0)
                        if porcentaje_actual is None:
                            porcentaje_actual = 0
                            
                        nuevo_porcentaje = st.slider(
                            "Porcentaje de Consumo",
                            min_value=0,
                            max_value=100,
                            value=int(porcentaje_actual),
                            key=f"slider_{idx}"
                        )
                        if nuevo_porcentaje != porcentaje_actual:
                            pass
                    
                    with col4:
                        if st.button("📸", key=f"btn_{idx}"):
                            st.camera_input(f"Foto vencimiento - {producto['Nombre']}", key=f"cam_{idx}")
                    
                    st.divider()
            
            with tab2:
                if productos:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.plotly_chart(create_category_chart(productos), use_container_width=True)
                        st.plotly_chart(create_cost_chart(productos), use_container_width=True)
                    
                    with col2:
                        st.plotly_chart(create_consumption_chart(productos), use_container_width=True)
                        
                        st.subheader("Resumen General")
                        total_productos = len(productos)
                        total_costo = sum(p.get('Costo', 0) for p in productos)
                        consumo_promedio = sum(p.get('PorcentajeConsumo', 0) if p.get('PorcentajeConsumo') is not None else 0 for p in productos) / total_productos if total_productos > 0 else 0
                        
                        col_stats1, col_stats2, col_stats3 = st.columns(3)
                        with col_stats1:
                            st.metric("Total Productos", total_productos)
                        with col_stats2:
                            st.metric("Costo Total", f"${total_costo:.2f}")
                        with col_stats3:
                            st.metric("Consumo Promedio", f"{consumo_promedio:.1f}%")
                else:
                    st.info("No hay datos suficientes para mostrar estadísticas.")
                    
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return