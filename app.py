import streamlit as st
import pandas as pd
import joblib

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Predicción Precio Autos", page_icon="🚗")

# --- 1. CARGAR EL MODELO ---
@st.cache_resource
def load_model():
    # Asegúrate de que el nombre coincida con tu archivo en GitHub
    return joblib.load('modelo_autos.pkl')

try:
    model = load_model()
except:
    st.error("⚠ Error: No se encuentra el archivo 'modelo_autos.pkl'. Verifica que esté subido a GitHub.")
    st.stop()

# --- 2. INTERFAZ: TÍTULO ---
st.title('🚗 Calculadora de Precio de Autos')
st.markdown("Ingresa los datos del vehículo para estimar su valor de venta.")

# --- 3. FORMULARIO DE DATOS (Sidebar) ---
st.sidebar.header('Datos del Auto')

def user_input_features():
    # Variables Numéricas
    anio = st.sidebar.slider('Año del Modelo', 2000, 2025, 2018)
    kms = st.sidebar.number_input('Kilometraje (kms)', min_value=0, value=50000)
    
    # Precio actual en concesionario (Present Price) - Dato importante para la predicción
    precio_lista = st.sidebar.number_input('Precio de Lista Nuevo (en miles $)', min_value=1.0, value=10.0)
