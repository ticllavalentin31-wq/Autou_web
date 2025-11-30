import os
import streamlit as st
import pandas as pd
import joblib
st.write("📂 Archivos detectados en la carpeta actual:")
st.write(os.listdir()) # Esto imprimirá la lista real de archivos que ve la App
st.set_page_config(page_title="Predicción Avanzada Autos", page_icon="🏎")

# 1. Cargar Modelo
@st.cache_resource
def load_model():
    return joblib.load('modelo_autos_avanzado.pkl')

try:
    model = load_model()
except:
    st.error("Sube el archivo 'modelo_autos_avanzado.pkl' a GitHub")
    st.stop()

st.title("🏎 Tasador de Autos con IA")

# 2. Formulario Inteligente
st.sidebar.header("Características")

# Necesitamos replicar las columnas exactas. 
# Como no tenemos el CSV aquí, pondremos las opciones más comunes manualmente
# o usaremos cajas de texto para simplificar.

def user_input_features():
    # Variables Numéricas
    year = st.sidebar.slider('Año', 1990, 2025, 2015)
    odometer = st.sidebar.number_input('Kilometraje', value=50000)
    
    # Variables Categóricas (Basadas en cars-1k)
    manufacturer = st.sidebar.selectbox('Fabricante', 
        ['ford', 'honda', 'toyota', 'nissan', 'chevrolet', 'jeep', 'ram', 'gmc', 'dodge', 'bmw', 'mercedes', 'audi', 'otros'])
    
    # El modelo es difícil de listar completo, usamos texto libre o genérico
    car_model = st.sidebar.text_input('Modelo (ej: f-150, civic)', 'civic')
    
    condition = st.sidebar.selectbox('Condición', ['excellent', 'good', 'fair', 'like new', 'salvage'])
    fuel = st.sidebar.selectbox('Combustible', ['gas', 'diesel', 'hybrid', 'electric'])
    transmission = st.sidebar.selectbox('Transmisión', ['automatic', 'manual', 'other'])
    drive = st.sidebar.selectbox('Tracción', ['4wd', 'fwd', 'rwd'])
    type_car = st.sidebar.selectbox('Tipo', ['sedan', 'SUV', 'pickup', 'truck', 'coupe', 'hatchback'])
    paint_color = st.sidebar.selectbox('Color', ['white', 'black', 'silver', 'grey', 'blue', 'red', 'custom'])

    # Crear DataFrame
    data = {
        'year': year,
        'manufacturer': manufacturer,
        'model': car_model,
        'condition': condition,
        'fuel': fuel,
        'odometer': odometer,
        'title_status': 'clean', # Valor por defecto
        'transmission': transmission,
        'drive': drive,
        'type': type_car,
        'paint_color': paint_color
    }
    return pd.DataFrame(data, index=[0])

input_df = user_input_features()

st.write("Datos ingresados:", input_df)

if st.button("Predecir Precio"):
    try:
        prediction = model.predict(input_df)
        st.success(f"Precio estimado: ${prediction[0]:,.2f}")
    except Exception as e:
        st.error(f"Error: {e}")
