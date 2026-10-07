import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import rasterio
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
# Usamos "wide" para aprovechar la pantalla, pero centraremos los elementos con columnas espaciadoras.
st.set_page_config(page_title="Monitor GBG", page_icon="🪰", layout="wide", initial_sidebar_state="collapsed")

# Forzar Tema Claro
st.markdown("""
    <style>
        .reportview-container { background-color: #FAFAFA; }
        .sidebar .sidebar-content { background-color: #F0F2F6; }
    </style>
""", unsafe_allow_html=True)

st.title("🪰 Monitor Epidemiológico: Gusano Barrenador del Ganado (GBG)")
st.markdown("Plataforma analítica para el rastreo y predicción espacial de brotes en México y Centroamérica.")
st.markdown("---")

# --- RUTAS DINÁMICAS ---
directorio_notebooks = os.getcwd()
directorio_raiz = os.path.dirname(directorio_notebooks)

ruta_area = os.path.join(directorio_raiz, 'data', 'processed', 'Datos_Catorcenas_2025.csv') 
ruta_combo = os.path.join(directorio_raiz, 'data', 'processed', 'Datos_Clima_Mensual.csv') 
ruta_mapa = os.path.join(directorio_raiz, 'data', 'processed', 'Datos_Mapa_Burbujas.csv') 
ruta_raster = os.path.join(directorio_raiz, 'data', 'processed', 'Mapa_Riesgo_Barrenador_2026.tif')

# --- 2. DINÁMICA TEMPORAL DE LA INFECCIÓN ---
st.header("📈 Dinámica Temporal de la Infección")

try:
    df_area = pd.read_csv(ruta_area)
    col_x = df_area.columns[0]
    col_y = df_area.columns[1]
    
    fig_area = px.area(
        df_area, 
        x=col_x, 
        y=col_y,
        color_discrete_sequence=['#B38481'] 
    )
    fig_area.update_traces(mode='lines+markers', marker=dict(color='#6B1C23'))
    fig_area.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=350, title="Infectados activos en periodos de 14 días (2025)")
    
    # ENVOLTURA PARA CENTRAR LA GRÁFICA
    espacio_izq, col_central, espacio_der = st.columns([1, 4, 1])
    with col_central:
        st.plotly_chart(fig_area, use_container_width=True)
        st.info("💡 **Interpretación:** Esta curva muestra los picos estacionales de los brotes en lapsos de catorce días. Permite identificar los meses donde la tasa de reproducción del parásito se acelera exponencialmente. Podemos identificar una aproximación de los casos activos en cada uno de los periodos de 14 días en el año 2025.")
    
except Exception as e:
    st.warning("No se pudo cargar la gráfica de áreas. Verifica el archivo.")

st.markdown("<br>", unsafe_allow_html=True) 

# --- 3. ANÁLISIS CLIMÁTICO ---
try:
    df_combo = pd.read_csv(ruta_combo)
    
    col_mes = df_combo.columns[0]
    col_casos = df_combo.columns[1]
    col_temp = df_combo.columns[2]
    col_lluvia = df_combo.columns[3]

    fig_combo = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_combo.add_trace(go.Bar(x=df_combo[col_mes], y=df_combo[col_casos], name='Casos Confirmados', marker_color='#A33A36'), secondary_y=False)
    fig_combo.add_trace(go.Scatter(x=df_combo[col_mes], y=df_combo[col_temp], name='Temperatura Promedio (°C)', line=dict(color='black', width=3)), secondary_y=True)
    fig_combo.add_trace(go.Scatter(x=df_combo[col_mes], y=df_combo[col_lluvia], name='Lluvia Promedio (mm)', line=dict(color='#E56B3A', width=3)), secondary_y=True)
    
    fig_combo.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=400, title="Influencia de la Humedad y Temperatura (2024-2025)", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    
    # ENVOLTURA PARA CENTRAR LA GRÁFICA
    espacio_izq, col_central, espacio_der = st.columns([1, 4, 1])
    with col_central:
        st.plotly_chart(fig_combo, use_container_width=True)
        st.info("💡 **Interpretación:** Observa la relación directa entre los aumentos de precipitación (línea naranja) y las caídas térmicas (línea negra) con la explosión de casos confirmados (barras rojas). La dependencia de la cantidad de casos con las variables climáticas se puede observar claramente con el comportamiento de la gráfica.")
    
except Exception as e:
    st.warning("No se pudo cargar la gráfica climática.")

st.markdown("---")

# --- 4. MAPA CON CLÚSTERES ---
st.header("🌍 Distribución Geográfica de Casos (Clustering)")
st.write("Explora el mapa. Los círculos indican agrupaciones de casos. **Haz zoom o clic en un círculo** para desagrupar y ver las ubicaciones exactas.")

try:
    df_mapa = pd.read_csv(ruta_mapa)
    
    col_lat = 'Latitud' 
    col_lon = 'Longitud'
    col_casos = 'Primera fecha: Municipio'     
    
    df_mapa = df_mapa.dropna(subset=[col_lat, col_lon])

    m = folium.Map(location=[17.5, -92.5], zoom_start=5, tiles='OpenStreetMap')
    marcador_cluster = MarkerCluster().add_to(m)

    for idx, fila in df_mapa.iterrows():
        lat = fila[col_lat]
        lon = fila[col_lon]
        texto_info = f"Casos: {fila[col_casos]}" if col_casos in df_mapa.columns else f"Lat: {lat}"
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=6, 
            color='#6B1C23',
            fill=True,
            fill_color='#A33A36',
            fill_opacity=0.7,
            popup=texto_info
        ).add_to(marcador_cluster)

    # ENVOLTURA PARA CENTRAR EL MAPA
    espacio_izq, col_central, espacio_der = st.columns([1, 4, 1])
    with col_central:
        st_folium(m, width=900, height=500, returned_objects=[])

except Exception as e:
    st.error(f"Error cargando el mapa de agrupamientos. Detalles técnicos: {e}")

st.markdown("---")

# --- 5. CONTENCIÓN Y NICHO BIOCLIMÁTICO ---
st.header("🔬 Contención Biológica y Análisis del Nicho")

st.success("""
**🦟 Técnica del Insecto Estéril (TIE)**  

Aunque el mapa proyecta un alto riesgo bioclimático, el escenario real está siendo mitigado activamente. 
Las autoridades sanitarias implementan la dispersión aérea de millones de **moscas macho esterilizadas** con radiación. 

Al aparearse con las hembras salvajes, estas no dejan descendencia, colapsando la población natural del parásito y reduciendo drásticamente el riesgo de expansión masiva que el modelo puramente climático sugeriría.
""")

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric(label="Riesgo Climático", value="Alto", delta="Condiciones Ideales", delta_color="inverse")
col_m2.metric(label="Riesgo Real", value="Controlado", delta="Dispersión de TIE")
col_m3.metric(label="Patrón Descubierto", value="Nicho Definido", delta="Modelo XGBoost", delta_color="off")

st.markdown("<br>", unsafe_allow_html=True)
st.write("**El Espacio de Supervivencia (Temperatura vs Humedad)**")

try:
    ruta_completa = os.path.join(directorio_raiz, 'data', 'processed', 'Dataset_GB_Mediana_Final.csv')
    df_completo = pd.read_csv(ruta_completa)
    
    df_completo['Fecha_Inicio'] = pd.to_datetime(df_completo['Fecha_Inicio'])
    df_completo['Mes'] = df_completo['Fecha_Inicio'].dt.month
    
    col_temp = 'Temperatura_Mediana_C' 
    col_lluvia = 'Precipitacion_Mediana_mm' 
    
    df_completo['Temp_Round'] = df_completo[col_temp].round(0)
    df_completo['Lluvia_Round'] = df_completo[col_lluvia].round(-1)
    
    df_3d = df_completo.groupby(['Temp_Round', 'Lluvia_Round', 'Mes']).size().reset_index(name='Concentracion')
    
    fig_3d = px.scatter_3d(
        df_3d, 
        x='Temp_Round',  
        y='Lluvia_Round',       
        z='Mes',          
        color='Concentracion',    
        size='Concentracion',
        color_continuous_scale='YlOrRd',
        opacity=0.9
    )
    
    fig_3d.update_layout(
        margin=dict(l=0, r=0, b=0, t=0), 
        height=600, 
        scene=dict(xaxis_title='Temp (°C)', yaxis_title='Lluvia (mm)', zaxis_title='Mes')
    )
    
    # ENVOLTURA PARA CENTRAR EL GRÁFICO 3D
    espacio_izq, col_central, espacio_der = st.columns([1, 4, 1])
    with col_central:
        st.plotly_chart(fig_3d, use_container_width=True)
    
except Exception as e:
    st.warning(f"Asegúrate de ajustar los nombres de las columnas para ver el gráfico 3D. Error: {e}")

st.markdown("---")

# --- 6. MAPA PREDICTIVO ---
st.header("🗺️ Proyección Espacial de Riesgo (Modelo XGBoost)")
st.write("A diferencia del mapa superior que muestra el pasado, este tensor espacial muestra la idoneidad bioclimática proyectada. Las zonas en rojo oscuro poseen el clima perfecto para la supervivencia endémica del parásito. Para el muestreo de idoneidad climática se han utilizado la mediana de la temperatura, así como una precipitación acumulada anual en cada zona. La predicción es sobre condiciones climáticas usuales en los territorios.")

try:
    with rasterio.open(ruta_raster) as src:
        matriz_riesgo = src.read(1)
        matriz_riesgo = np.where(matriz_riesgo == src.nodata, np.nan, matriz_riesgo)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        im = ax.imshow(matriz_riesgo, cmap='YlOrRd', vmin=0, vmax=1)
        ax.axis('off')
        cbar = plt.colorbar(im, ax=ax, fraction=0.036, pad=0.04)
        cbar.set_label('Probabilidad de Supervivencia', rotation=270, labelpad=20)
        
        # ENVOLTURA PARA CENTRAR EL MAPA PREDICTIVO
        espacio_izq, col_central, espacio_der = st.columns([1, 4, 1])
        with col_central:
            st.pyplot(fig)
            
except Exception as e:
    st.info("Coloca tu mapa .tif en la ruta especificada para visualizar la predicción.")