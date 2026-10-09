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
st.set_page_config(page_title="Monitor GBG", page_icon="🪰", layout="wide", initial_sidebar_state="expanded")

# --- RUTAS DINÁMICAS ---
ruta_actual = os.path.abspath(__file__)
directorio_raiz = os.path.dirname(os.path.dirname(ruta_actual))

ruta_area = os.path.join(directorio_raiz, 'data', 'processed', 'Datos_Catorcenas_2025.csv') 
ruta_combo = os.path.join(directorio_raiz, 'data', 'processed', 'Datos_Clima_Mensual.csv') 
ruta_mapa = os.path.join(directorio_raiz, 'data', 'processed', 'Datos_Mapa_Burbujas.csv') 
ruta_raster = os.path.join(directorio_raiz, 'data', 'processed', 'Mapa_Riesgo_Barrenador_2026.tif')
ruta_completa = os.path.join(directorio_raiz, 'data', 'processed', 'Dataset_GB_Mediana_Final.csv')

# --- 2. MENÚ LATERAL DE NAVEGACIÓN ---
with st.sidebar:
    # URL directa de alta resolución y más estable
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/89/Cochliomyia_hominivorax.jpg", use_column_width=True) 
    st.title("Navegación")
    opcion = st.radio(
        "Selecciona un módulo:",
        ("📖 Panorama General", "📊 Análisis Epidemiológico", "🌍 Inteligencia Geoespacial", "⚙️ Metodología y Simulador")
    )
    st.markdown("---")
    st.caption("Desarrollado por Moises Segura Carrillo")
    st.caption("Facultad de Ciencias Físico-Matemáticas, BUAP")

# --- 3. CONTENIDO DE LAS PÁGINAS ---

if opcion == "📖 Panorama General":
    st.title("🪰 Monitor Epidemiológico: Gusano Barrenador del Ganado")
    st.markdown("Plataforma analítica para el rastreo y predicción espacial de brotes en México y Centroamérica.")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("¿Qué es el Gusano Barrenador?")
        st.write("""
        El **Gusano Barrenador del Ganado (*Cochliomyia hominivorax*)** es un parásito altamente destructivo. 
        Las moscas hembra depositan sus huevos en heridas abiertas de animales de sangre caliente. 
        Al eclosionar, las larvas se alimentan del tejido vivo, causando miasis severa y, en casos extremos, la muerte del huésped.
        Tras décadas de erradicación, la plaga ha reingresado a Centroamérica, amenazando la industria ganadera y la salud pública de México, alcanzando grandes infecciones en el año 2025.
	La mosca puede volar distancias grandes cuando el clima es favorable buscando dónde poner sus huevos. Es muy sensible al frío, el clima es el factor más importante para analizar la supervivencia del animal.
	Tras el aumento de casos en México desde 2024, en Mayo del 2025 Estados Unidos (E.E.U.U) anunció la suspensión total e inmediata de entrada de ganado vivo. Las exportaciones de ganado para México cayeron causando pérdidas económicas importantes para el país.
        """)
        
    with col2:
        st.info("**Datos Clave:**\n\n"
                "🌡️ **Clima:** Requiere calor y humedad alta.\n\n"
                "🛑 **Riesgo:** Expansión rápida sin cercos sanitarios.\n\n"
                "🐄 **Impacto:** Pérdidas millonarias en ganadería.")
        
    st.subheader("La Barrera Artificial: Técnica del Insecto Estéril (TIE)")
    st.success("""
    Aunque nuestro modelo proyecta un alto riesgo bioclimático, el escenario real está siendo mitigado activamente. 
    Las autoridades sanitarias implementan la dispersión aérea de millones de **moscas macho esterilizadas** con radiación. 
    Al aparearse con las hembras salvajes, estas no dejan descendencia, colapsando la población natural del parásito y reduciendo drásticamente el riesgo de expansión masiva.
    """)

elif opcion == "📊 Análisis Epidemiológico":
    st.title("📊 Análisis Epidemiológico e Influencia Climática")
    st.markdown("---")
    
    st.subheader("Dinámica Temporal de la Infección")
    try:
        df_area = pd.read_csv(ruta_area)
        fig_area = px.area(df_area, x=df_area.columns[0], y=df_area.columns[1], color_discrete_sequence=['#B38481'])
        fig_area.update_traces(mode='lines+markers', marker=dict(color='#6B1C23'))
        fig_area.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        
        esp_izq, col_c, esp_der = st.columns([1, 4, 1])
        with col_c:
            st.plotly_chart(fig_area, use_container_width=True)
            st.info("💡 **Interpretación:** Esta curva muestra los picos estacionales de los brotes en lapsos de catorce días (tiempo aproximado del peligro en el animal infectado). Permite identificar los meses donde la tasa de reproducción del parásito se acelera exponencialmente.")
    except: st.warning("No se pudo cargar la gráfica de áreas.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Correlación Clima-Infección (2024-2025)")
    try:
        df_combo = pd.read_csv(ruta_combo)
        col_mes, col_casos, col_temp, col_lluvia = df_combo.columns[0], df_combo.columns[1], df_combo.columns[2], df_combo.columns[3]
        fig_combo = make_subplots(specs=[[{"secondary_y": True}]])
        fig_combo.add_trace(go.Bar(x=df_combo[col_mes], y=df_combo[col_casos], name='Casos', marker_color='#A33A36'), secondary_y=False)
        fig_combo.add_trace(go.Scatter(x=df_combo[col_mes], y=df_combo[col_temp], name='Temp (°C)', line=dict(color='black', width=3)), secondary_y=True)
        fig_combo.add_trace(go.Scatter(x=df_combo[col_mes], y=df_combo[col_lluvia], name='Lluvia (mm)', line=dict(color='#E56B3A', width=3)), secondary_y=True)
        fig_combo.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        
        esp_izq, col_c, esp_der = st.columns([1, 4, 1])
        with col_c:
            st.plotly_chart(fig_combo, use_container_width=True)
            st.info("💡 **Interpretación:** Observa la relación directa entre los aumentos de precipitación (línea naranja) y las caídas térmicas (línea negra) con la explosión de casos confirmados (barras rojas).")
    except: st.warning("No se pudo cargar la gráfica climática.")

    st.markdown("---")
    st.subheader("El Espacio de Supervivencia 3D (Nicho Biológico)")
    try:
        df_completo = pd.read_csv(ruta_completa)
        df_completo['Fecha_Inicio'] = pd.to_datetime(df_completo['Fecha_Inicio'])
        df_completo['Mes'] = df_completo['Fecha_Inicio'].dt.month
        col_temp, col_lluvia = 'Temperatura_Mediana_C', 'Precipitacion_Mediana_mm' 
        df_completo['Temp_Round'] = df_completo[col_temp].round(0)
        df_completo['Lluvia_Round'] = df_completo[col_lluvia].round(-1)
        df_3d = df_completo.groupby(['Temp_Round', 'Lluvia_Round', 'Mes']).size().reset_index(name='Concentracion')
        
        fig_3d = px.scatter_3d(df_3d, x='Temp_Round', y='Lluvia_Round', z='Mes', color='Concentracion', size='Concentracion', color_continuous_scale='YlOrRd', opacity=0.9)
        fig_3d.update_layout(margin=dict(l=0, r=0, b=0, t=0), height=500, scene=dict(xaxis_title='Temp (°C)', yaxis_title='Lluvia (mm)', zaxis_title='Mes'), paper_bgcolor="rgba(0,0,0,0)")
        
        esp_izq, col_c, esp_der = st.columns([1, 4, 1])
        with col_c: 
            st.plotly_chart(fig_3d, use_container_width=True)
            st.info("💡 **Interpretación:** Esta gráfica tridimensional materializa el 'Nicho Ecológico Fundamental'. Las esferas más grandes y oscuras representan el rango térmico y pluviométrico exacto donde la plaga encuentra las condiciones biológicas perfectas para detonar brotes masivos.")
    except: st.warning("No se pudo cargar el gráfico 3D.")

elif opcion == "🌍 Inteligencia Geoespacial":
    st.title("🌍 Inteligencia Geoespacial")
    st.markdown("---")
    
    st.subheader("Histórico: Agrupamiento Espacial de Brotes (Clustering)")
    st.write("Explora el mapa interactivo haciendo zoom sobre los focos de infección registrados.")
    try:
        df_mapa = pd.read_csv(ruta_mapa)
        col_lat, col_lon, col_casos = 'Latitud', 'Longitud', 'Primera fecha: Municipio'     
        df_mapa = df_mapa.dropna(subset=[col_lat, col_lon])

        m = folium.Map(location=[17.5, -92.5], zoom_start=5, tiles='OpenStreetMap')
        marcador_cluster = MarkerCluster().add_to(m)

        for idx, fila in df_mapa.iterrows():
            lat, lon = fila[col_lat], fila[col_lon]
            texto_info = f"Casos: {fila[col_casos]}" if col_casos in df_mapa.columns else f"Lat: {lat}"
            folium.CircleMarker(location=[lat, lon], radius=6, color='#6B1C23', fill=True, fill_color='#A33A36', fill_opacity=0.7, popup=texto_info).add_to(marcador_cluster)

        esp_izq, col_c, esp_der = st.columns([1, 4, 1])
        with col_c: 
            st_folium(m, width=900, height=500, returned_objects=[])
            st.info("💡 **Interpretación:** Este mapa muestra los clústeres históricos de infección. Las burbujas indican zonas que ya sufrieron epidemias severas, marcando visualmente los corredores geográficos por donde avanza el parásito.")
    except: st.error("Error cargando el mapa de agrupamientos.")

    st.markdown("---")
    st.subheader("Futuro: Proyección Espacial de Riesgo (XGBoost 2026)")
    st.write("Tensor de idoneidad bioclimática proyectada por nuestro modelo de Machine Learning.")
    try:
        with rasterio.open(ruta_raster) as src:
            matriz_riesgo = src.read(1)
            matriz_riesgo = np.where(matriz_riesgo == src.nodata, np.nan, matriz_riesgo)
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Cambiamos el fondo de la figura para que coincida con la página
            fig.patch.set_facecolor('#F4F6F9') 
            
            im = ax.imshow(matriz_riesgo, cmap='YlOrRd', vmin=0, vmax=1)
            ax.axis('off')
            cbar = plt.colorbar(im, ax=ax, fraction=0.036, pad=0.04)
            cbar.set_label('Probabilidad de Supervivencia', rotation=270, labelpad=20)
            
            esp_izq, col_c, esp_der = st.columns([1, 4, 1])
            with col_c: 
                st.pyplot(fig)
                st.info("💡 **Interpretación:** A diferencia del mapa superior (pasado), este tensor evalúa el riesgo a futuro. Las zonas en rojo oscuro poseen el clima perfecto para la supervivencia endémica, indicando dónde deben enfocarse las barreras de insectos estériles antes de que la plaga llegue.")
    except: st.info("Cargando proyección raster...")

elif opcion == "⚙️ Metodología y Simulador":
    st.title("⚙️ Arquitectura del Modelo y Simulador")
    st.markdown("---")
    
    col_text, col_sim = st.columns([1.2, 1])
    
    with col_text:
        st.subheader("Ingeniería de Características")
        st.write("""
        Para entrenar el modelo predictivo de Nicho Ecológico, se tomaron dos decisiones estadísticas fundamentales:
        
        1. **Uso de la Mediana Climática:** Se comprimieron dos años de registros climáticos utilizando la mediana en lugar del promedio. Esto elimina el ruido de anomalías estocásticas (olas de calor o tormentas atípicas de pocos días) y revela la verdadera "firma climática base" de la región.
        2. **Generación de Pseudo-ausencias:** Al solo contar con registros de infecciones positivas, se utilizó un muestreo espacial de pseudo-ausencias. Esto le permite al algoritmo XGBoost aprender el contraste entre un clima ideal (presencia) y un clima hostil, logrando una clasificación de riesgo robusta (AUC > 0.92).
        """)
        
    with col_sim:
        st.subheader("🧪 Simulador Bioclimático Rápido")
        st.write("Mueve los deslizadores para evaluar teóricamente el riesgo basado en el comportamiento del clúster 3D.")
        
        temp_input = st.slider("Temperatura Promedio (°C)", min_value=10.0, max_value=40.0, value=25.0, step=0.5)
        lluvia_input = st.slider("Precipitación Promedio (mm)", min_value=0.0, max_value=300.0, value=120.0, step=5.0)
        
        if 20 <= temp_input <= 30 and lluvia_input >= 50:
            st.error("🚨 **Nivel de Riesgo: ALTO** \n\nCondiciones termopluviométricas óptimas para la reproducción masiva.")
        elif (15 <= temp_input < 20 or 30 < temp_input <= 35) and lluvia_input >= 20:
            st.warning("⚠️ **Nivel de Riesgo: MODERADO** \n\nSupervivencia posible, pero sin tasa de crecimiento exponencial.")
        else:
            st.success("✅ **Nivel de Riesgo: BAJO** \n\nCondiciones hostiles. Es improbable que la plaga se vuelva endémica aquí.")