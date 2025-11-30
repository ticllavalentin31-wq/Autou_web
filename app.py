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
    
    # Variables Categóricas (Texto)
    combustible = st.sidebar.selectbox('Combustible', ['Petrol', 'Diesel', 'CNG'])
    vendedor = st.sidebar.selectbox('Tipo de Vendedor', ['Dealer', 'Individual'])
    transmision = st.sidebar.selectbox('Transmisión', ['Manual', 'Automatic'])
    duenos = st.sidebar.selectbox('Dueños Anteriores', [0, 1, 3])

    # --- PREPROCESAMIENTO INTERNO ---
    # Convertimos texto a números igual que en el entrenamiento
    # Combustible: Petrol=0, Diesel=1, CNG=2
    fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}
    
    # Vendedor: Dealer=0, Individual=1
    seller_map = {'Dealer': 0, 'Individual': 1}
    
    # Transmisión: Manual=0, Automatic=1
    trans_map = {'Manual': 0, 'Automatic': 1}

    # Crear el DataFrame con los nombres EXACTOS de las columnas de entrenamiento
    data = {
        'Year': anio,
        'Present_Price': precio_lista,
        'Kms_Driven': kms,
        'Fuel_Type': fuel_map[combustible],
        'Seller_Type': seller_map[vendedor],
        'Transmission': trans_map[transmision],
        'Owner': duenos
    }
    
    return pd.DataFrame(data, index=[0])

# Capturar datos
df_input = user_input_features()

# Mostrar resumen al usuario
st.subheader('Resumen del vehículo:')
st.table(df_input)

# --- 4. BOTÓN DE PREDICCIÓN ---
if st.button('💰 Calcular Precio'):
    try:
        prediction = model.predict(df_input)
        st.success(f"El precio estimado es: ${prediction[0]:,.2f} USD")
    except Exception as e:
        st.error(f"Error al predecir: {e}")
        st.info("Nota: Revisa que el archivo 'modelo_autos.pkl' se haya creado con las mismas columnas.")
