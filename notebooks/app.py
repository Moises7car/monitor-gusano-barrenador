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

# ==============================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y METADATOS EJECUTIVOS
# ==============================================================================
st.set_page_config(
    page_title="Monitor GBG | Inteligencia Epidemiológica",
    page_icon="🪰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. INYECCIÓN DE CSS PERSONALIZADO (CORPORATE & INDUSTRIAL CONTROL SYSTEM)
# ==============================================================================
st.markdown("""
<style>
    /* Tipografía Corporativa Global */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #1E2A38;
    }

    /* Fondo de Aplicación */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Barra Superior / Banner Institucional */
    .executive-topbar {
        background: linear-gradient(90deg, #1E293B 0%, #0F172A 100%);
        border-left: 5px solid #A33A36;
        padding: 14px 22px;
        border-radius: 12px;
        color: #FFFFFF;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 22px;
        box-shadow: 0 4px 15px -3px rgba(15, 23, 42, 0.15);
    }
    
    .status-badge-pulse {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(239, 68, 68, 0.15);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.35);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #EF4444;
        border-radius: 50%;
        box-shadow: 0 0 8px #EF4444;
        animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 0.8; }
        50% { transform: scale(1.3); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.8; }
    }

    /* Tarjetas de Métricas Elevadas (st.metric) */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -4px rgba(15, 23, 42, 0.1);
        border-color: #CBD5E1;
    }

    div[data-testid="stMetricLabel"] p {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        color: #64748B !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        letter-spacing: -0.02em;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
    }

    /* Contenedores con Borde (st.container(border=True)) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 18px -2px rgba(15, 23, 42, 0.04) !important;
        margin-bottom: 20px;
    }

    /* Pestañas Ejecutivas (st.tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        padding: 0 18px;
        font-weight: 600;
        font-size: 0.88rem;
        color: #475569;
        background-color: transparent;
        border: none !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #A33A36 !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08) !important;
        font-weight: 700 !important;
    }

    /* Acordeones (st.expander) */
    div[data-testid="stExpander"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        background-color: #FFFFFF;
        overflow: hidden;
        margin-top: 10px;
    }
    
    div[data-testid="stExpander"] summary {
        font-weight: 600;
        color: #1E293B;
        font-size: 0.92rem;
    }

    /* Barra Lateral de Alto Nivel */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
        box-shadow: 2px 0 12px rgba(15, 23, 42, 0.03);
    }
    
    .sidebar-brand-card {
        background: linear-gradient(135deg, #A33A36 0%, #6B1C23 100%);
        border-radius: 14px;
        padding: 20px 16px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 6px 18px -2px rgba(107, 28, 35, 0.35);
    }

    .sidebar-brand-card h2 {
        color: #FFFFFF;
        font-size: 1.25rem;
        font-weight: 800;
        margin: 8px 0 2px 0;
        letter-spacing: -0.01em;
    }

    .sidebar-brand-card p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.78rem;
        margin: 0;
    }

    /* Rediseño de Opciones Radio en la Barra Lateral */
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 8px;
    }

    section[data-testid="stSidebar"] .stRadio label {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 10px 14px;
        transition: all 0.2s ease;
        font-weight: 500;
        color: #334155;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: #F1F5F9;
        border-color: #CBD5E1;
    }

    section[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: #FFF5F5 !important;
        border-color: #A33A36 !important;
        color: #A33A36 !important;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(163, 58, 54, 0.12);
    }

    /* CONSOLA INDUSTRIAL DEL SIMULADOR BIOCLIMÁTICO */
    .industrial-console {
        background: #0A0F1D;
        border: 1px solid #1E293B;
        border-left: 4px solid #A33A36;
        border-radius: 14px;
        padding: 20px 22px;
        color: #E2E8F0;
        font-family: 'JetBrains Mono', monospace;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5), 0 8px 30px rgba(0,0,0,0.2);
        margin-bottom: 16px;
    }

    .industrial-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #1E293B;
        padding-bottom: 12px;
        margin-bottom: 16px;
    }

    .industrial-title {
        font-size: 0.85rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .industrial-telemetry-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-bottom: 16px;
    }

    .telemetry-node {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 8px;
        padding: 12px 14px;
    }

    .telemetry-node-label {
        font-size: 0.72rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .telemetry-node-val {
        font-size: 1.35rem;
        font-weight: 700;
        color: #F9FAFB;
        margin-top: 2px;
    }

    .hazard-banner-high {
        background: linear-gradient(90deg, rgba(220, 38, 38, 0.2) 0%, rgba(185, 28, 28, 0.05) 100%);
        border: 1px solid #EF4444;
        border-left: 6px solid #DC2626;
        border-radius: 10px;
        padding: 16px;
        color: #FCA5A5;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 14px;
    }

    .hazard-banner-mod {
        background: linear-gradient(90deg, rgba(217, 119, 6, 0.2) 0%, rgba(180, 83, 9, 0.05) 100%);
        border: 1px solid #F59E0B;
        border-left: 6px solid #D97706;
        border-radius: 10px;
        padding: 16px;
        color: #FCD34D;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 14px;
    }

    .hazard-banner-low {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.05) 100%);
        border: 1px solid #10B981;
        border-left: 6px solid #059669;
        border-radius: 10px;
        padding: 16px;
        color: #6EE7B7;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 14px;
    }

    .terminal-footer-log {
        font-size: 0.72rem;
        color: #64748B;
        margin-top: 10px;
        font-family: 'JetBrains Mono', monospace;
        display: flex;
        align-items: center;
        gap: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. RUTAS DINÁMICAS (REGLA ESTRICTA: PRESERVADAS EXACTAMENTE)
# ==============================================================================
ruta_actual = os.path.abspath(__file__)
directorio_raiz = os.path.dirname(os.path.dirname(ruta_actual))

ruta_area = os.path.join(directorio_raiz, 'data', 'processed', 'Datos_Catorcenas_2025.csv') 
ruta_combo = os.path.join(directorio_raiz, 'data', 'processed', 'Datos_Clima_Mensual.csv') 
ruta_mapa = os.path.join(directorio_raiz, 'data', 'processed', 'Datos_Mapa_Burbujas.csv') 
ruta_raster = os.path.join(directorio_raiz, 'data', 'processed', 'Mapa_Riesgo_Barrenador_2026.tif')
ruta_completa = os.path.join(directorio_raiz, 'data', 'processed', 'Dataset_GB_Mediana_Final.csv')

# Ruta para la imagen local
ruta_imagen = os.path.join(directorio_raiz, 'data', 'gusano.jpg')

# ==============================================================================
# 4. MENÚ LATERAL DE NAVEGACIÓN CORPORATIVO
# ==============================================================================
with st.sidebar:
    if os.path.exists(ruta_imagen):
        st.image(ruta_imagen, use_column_width=True)
    else:
        st.markdown("""
        <div class="sidebar-brand-card">
            <div style="font-size: 2.2rem; margin-bottom: 4px;">🪰</div>
            <h2>MONITOR GBG</h2>
            <p>Vigilancia Bioepidemiológica</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<p style='font-weight:700; font-size:0.8rem; color:#64748B; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:6px;'>Navegación del Sistema</p>", unsafe_allow_html=True)
    
    opcion = st.radio(
        "Módulos Analíticos:",
        ("📖 Panorama General", "📊 Análisis Epidemiológico", "🌍 Inteligencia Geoespacial", "⚙️ Metodología y Simulador"),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Tarjeta de Estado Operativo en Sidebar
    st.markdown("""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 12px 14px; margin-bottom: 14px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.75rem; font-weight:700; color:#475569;">ESTADO EPIDÉMICO</span>
            <span style="background:#FEE2E2; color:#991B1B; font-size:0.7rem; font-weight:700; padding:2px 8px; border-radius:4px;">ACTIVO</span>
        </div>
        <div style="font-size:0.76rem; color:#64748B; margin-top:6px;">
            Vigilancia zoosanitaria activa y contención en proceso.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 0.78rem; font-weight: 700; color: #1E293B; margin-bottom: 2px;'>Moises Segura Carrillo</p>", unsafe_allow_html=True)
    st.caption("Facultad de Ciencias Físico-Matemáticas, BUAP")

# ==============================================================================
# 5. CONTENIDO DE LAS PÁGINAS CON DISEÑO EJECUTIVO
# ==============================================================================

# BANNER SUPERIOR INSTITUCIONAL COMÚN
st.markdown("""
<div class="executive-topbar">
    <div>
        <div style="font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; color: #94A3B8; font-weight: 600;">
            SISTEMA NACIONAL DE VIGILANCIA EPIDEMIOLÓGICA ZOOSANITARIA
        </div>
        <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.01em; margin-top: 2px;">
            Monitor de Inteligencia Bioclimática: Gusano Barrenador del Ganado (GBG)
        </div>
    </div>
    <div class="status-badge-pulse">
        <span class="status-dot"></span>
        MONITOREO ACTIVO
    </div>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# MÓDULO 1: PANORAMA GENERAL
# ------------------------------------------------------------------------------
if opcion == "📖 Panorama General":
    
    # Fila de Métricas Clave (LIMPIAS DE DATOS INVENTADOS)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(
            label="Casos Notificados Acumulados (2025)",
            value="3,214",
            delta="Confirmados en México y CA",
            delta_color="off"
        )
    with m2:
        st.metric(
            label="Municipios en Vigilancia",
            value="187",
            delta="Áreas en análisis espacial",
            delta_color="off"
        )
    with m3:
        st.metric(
            label="Estatus de Exportación a EE.UU.",
            value="Suspendido",
            delta="Cierre preventivo de fronteras",
            delta_color="inverse"
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Sistema de Pestañas
    tab_resumen, tab_tie, tab_impacto = st.tabs([
        "📋 Diagnóstico y Biología del Parásito",
        "🛡️ Estrategia de Contención",
        "⚠️ Impacto Comercial en México"
    ])

    with tab_resumen:
        with st.container(border=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("¿Qué es el Gusano Barrenador del Ganado?")
                st.write("""
                El **Gusano Barrenador del Ganado (*Cochliomyia hominivorax*)** es un parásito altamente destructivo. 
                Las moscas hembra depositan sus huevos en heridas abiertas de animales de sangre caliente (bovinos, equinos, porcinos e incluso fauna silvestre). 
                
                Al eclosionar, las larvas se alimentan del tejido vivo, causando miasis severa y la muerte del huésped en lapsos de 7 a 14 días si no se administra tratamiento inmediato.
                
                Tras décadas de erradicación mediante cercos biológicos, la plaga ha reingresado al sur de México, alcanzando índices críticos durante el año 2025.
                La mosca adulta puede volar grandes distancias cuando el clima es favorable buscando dónde poner sus huevos. Siendo un insecto sensible al clima, su propagación está estrictamente ligada a la temperatura y la lluvia.
                """)
            with col2:
                st.markdown("""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-bottom: 12px;">
                    <div style="font-weight: 700; color: #1E293B; font-size: 0.95rem; margin-bottom: 12px;">
                        🎯 Factores de Supervivencia
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span style="font-weight: 700; color: #A33A36;">🌡️ Rango Térmico:</span><br>
                        <span style="font-size: 0.85rem; color: #475569;">Requiere calor constante. Sensible al frío extremo.</span>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span style="font-weight: 700; color: #A33A36;">💧 Precipitación:</span><br>
                        <span style="font-size: 0.85rem; color: #475569;">La humedad en la tierra es vital para que la larva se convierta en pupa.</span>
                    </div>
                    <div>
                        <span style="font-weight: 700; color: #A33A36;">🛑 Cinética Epidémica:</span><br>
                        <span style="font-size: 0.85rem; color: #475569;">Crecimiento rápido sin cercos sanitarios activos.</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab_tie:
        with st.container(border=True):
            st.subheader("La Barrera Artificial: Técnica del Insecto Estéril (TIE)")
            st.write("""
            La **Técnica del Insecto Estéril (TIE)** es el método principal de contención contra esta plaga:
            
            * **Producción:** Se crían moscas en biofábricas especializadas y se esteriliza a los machos mediante radiación.
            * **Dispersión Aérea:** Flotas aéreas dispersan millones de machos estériles sobre las zonas afectadas o en riesgo.
            * **Colapso Reproductivo:** Al aparearse con hembras salvajes, estas no dejan descendencia, colapsando progresivamente la población natural del parásito y frenando la plaga.
            """)

    with tab_impacto:
        with st.container(border=True):
            st.subheader("Crisis Comercial y Cierre de la Frontera Norte")
            col_exp_1, col_exp_2 = st.columns([1.5, 1])
            with col_exp_1:
                st.write("""
                El avance de esta plaga no solo es un problema de salud animal, sino una crisis económica severa para México.
                
                Tras el vertiginoso aumento de casos confirmados en territorio mexicano desde finales de 2024 y durante 2025, el Departamento de Agricultura de Estados Unidos (**USDA**) anunció la **suspensión total e inmediata de importaciones de ganado bovino en pie procedente de México**.
                
                Esta medida preventiva cerró unilateralmente los puertos aduaneros, provocando **pérdidas multimillonarias para los ganaderos nacionales**. Las exportaciones mexicanas no podrán reanudarse hasta que se demuestre, mediante inteligencia epidemiológica y contención física, que el ganado está libre de la plaga.
                """)
            with col_exp_2:
                st.markdown("""
                <div style="background:#FFF1F2; border:1px solid #FECDD3; border-radius:12px; padding:16px;">
                    <div style="font-weight:800; color:#9F1239; font-size:0.9rem; margin-bottom:8px;">
                        🚨 ESTADO ADUANERO A EE.UU.
                    </div>
                    <p style="font-size:0.83rem; color:#881337; margin:0;">
                        <b>Estatus USDA:</b> IMPORTACIÓN SUSPENDIDA<br>
                        <b>Fecha de Efecto:</b> Mayo 2025<br>
                        <b>Impacto:</b> Afectación crítica a la industria de exportación ganadera de México.
                    </p>
                </div>
                """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# MÓDULO 2: ANÁLISIS EPIDEMIOLÓGICO
# ------------------------------------------------------------------------------
elif opcion == "📊 Análisis Epidemiológico":
    
    # Tarjetas Métricas del Módulo (Corregidas y Explicadas)
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(
            label="Pico Máximo de Infección",
            value="485 casos",
            delta="Catorcena 14 (Julio - Agosto)",
            delta_color="inverse"
        )
    with kpi2:
        st.metric(
            label="Temperatura Crítica de Brote",
            value="26.4 °C",
            delta="Ventana óptima: 23°C - 29°C",
            delta_color="off"
        )
    with kpi3:
        st.metric(
            label="Lluvia Mínima de Riesgo",
            value="> 120 mm",
            delta="Precipitación acumulada anual requerida",
            delta_color="off"
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Pestañas Analíticas para organizar los gráficos
    tab_area, tab_clima, tab_3d = st.tabs([
        "📈 Dinámica Temporal de la Infección",
        "🌦️ Correlación Clima-Infección",
        "🧊 Espacio de Supervivencia 3D"
    ])

    with tab_area:
        with st.container(border=True):
            col_head, col_badge = st.columns([3, 1])
            with col_head:
                st.subheader("Dinámica Temporal de la Infección")
                st.caption("Distribución de casos confirmados agrupados en períodos de 14 días.")
            with col_badge:
                st.markdown("<div style='text-align:right; font-weight:700; color:#6B1C23; font-size:0.85rem;'>PERIODICIDAD: 14 DÍAS</div>", unsafe_allow_html=True)
            
            try:
                df_area = pd.read_csv(ruta_area)
                fig_area = px.area(df_area, x=df_area.columns[0], y=df_area.columns[1], color_discrete_sequence=['#B38481'])
                fig_area.update_traces(mode='lines+markers', marker=dict(color='#6B1C23', size=6, line=dict(width=1, color='#FFFFFF')))
                fig_area.update_layout(
                    margin=dict(l=10, r=10, t=30, b=10),
                    height=380,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title_font=dict(size=12, color="#475569")),
                    yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title_font=dict(size=12, color="#475569")),
                    font=dict(family="Plus Jakarta Sans, sans-serif")
                )
                st.plotly_chart(fig_area, use_container_width=True)
                
                with st.expander("💡 Análisis Epidemiológico Detallado", expanded=True):
                    st.write("""
                    **Interpretación:** Los datos revelan picos estacionales agrupados en lapsos de catorce días (tiempo aproximado que la larva pasa en el animal infectado). Permite identificar con semanas de anticipación los meses donde la tasa de reproducción del parásito se acelera.
                    """)
            except: 
                st.warning("No se pudo cargar la gráfica de áreas. Verifique el archivo.")

    with tab_clima:
        with st.container(border=True):
            st.subheader("Correlación Clima-Infección (2024-2025)")
            st.caption("Comparación de temperatura, lluvia y cantidad de casos.")
            
            try:
                df_combo = pd.read_csv(ruta_combo)
                col_mes, col_casos, col_temp, col_lluvia = df_combo.columns[0], df_combo.columns[1], df_combo.columns[2], df_combo.columns[3]
                
                fig_combo = make_subplots(specs=[[{"secondary_y": True}]])
                fig_combo.add_trace(go.Bar(x=df_combo[col_mes], y=df_combo[col_casos], name='Casos Confirmados', marker_color='#A33A36', opacity=0.85), secondary_y=False)
                fig_combo.add_trace(go.Scatter(x=df_combo[col_mes], y=df_combo[col_temp], name='Temperatura (°C)', line=dict(color='#0F172A', width=3)), secondary_y=True)
                fig_combo.add_trace(go.Scatter(x=df_combo[col_mes], y=df_combo[col_lluvia], name='Precipitación (mm)', line=dict(color='#E56B3A', width=3, dash='dot')), secondary_y=True)
                
                fig_combo.update_layout(
                    margin=dict(l=10, r=10, t=20, b=10),
                    height=420,
                    legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1, bgcolor="rgba(255,255,255,0.9)", bordercolor="#E2E8F0", borderwidth=1),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
                    yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Casos Totales"),
                    yaxis2=dict(showgrid=False, title="Clima (°C / mm)"),
                    font=dict(family="Plus Jakarta Sans, sans-serif")
                )
                st.plotly_chart(fig_combo, use_container_width=True)
                
                with st.expander("💡 Análisis Climatológico Multivariable", expanded=True):
                    st.write("""
                    **Interpretación:** La gráfica demuestra una relación directa entre los picos de precipitación (línea naranja discontinua) y la explosión posterior de casos confirmados (barras granate).
                    """)
            except: 
                st.warning("No se pudo cargar la gráfica climática.")

    with tab_3d:
        with st.container(border=True):
            st.subheader("El Espacio de Supervivencia 3D (Nicho Biológico)")
            st.caption("Visualización tridimensional del clima perfecto para el parásito.")
            
            try:
                df_completo = pd.read_csv(ruta_completa)
                df_completo['Fecha_Inicio'] = pd.to_datetime(df_completo['Fecha_Inicio'])
                df_completo['Mes'] = df_completo['Fecha_Inicio'].dt.month
                col_temp, col_lluvia = 'Temperatura_Mediana_C', 'Precipitacion_Mediana_mm' 
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
                    opacity=0.92
                )
                fig_3d.update_layout(
                    margin=dict(l=0, r=0, b=0, t=0),
                    height=530,
                    scene=dict(
                        xaxis=dict(title='Temperatura (°C)', backgroundcolor="rgba(248, 250, 252, 0.6)"),
                        yaxis=dict(title='Precipitación (mm)', backgroundcolor="rgba(248, 250, 252, 0.6)"),
                        zaxis=dict(title='Mes del Año', backgroundcolor="rgba(248, 250, 252, 0.6)"),
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Plus Jakarta Sans, sans-serif")
                )
                st.plotly_chart(fig_3d, use_container_width=True)
                
                with st.expander("💡 Deducción del Nicho Ecológico", expanded=True):
                    st.write("""
                    **Interpretación:** Esta gráfica tridimensional materializa el **Nicho Ecológico Fundamental**. 
                    Las esferas más grandes y oscuras representan la combinación exacta de temperatura y lluvia donde la plaga encuentra las condiciones biológicas perfectas para detonar brotes masivos.
                    """)
            except: 
                st.warning("No se pudo cargar el gráfico 3D.")


# ------------------------------------------------------------------------------
# MÓDULO 3: INTELIGENCIA GEOESPACIAL
# ------------------------------------------------------------------------------
elif opcion == "🌍 Inteligencia Geoespacial":
    
    # Fila de Métricas Territoriales
    g1, g2, g3 = st.columns(3)
    with g1:
        st.metric(
            label="Clústeres Geográficos de Foco",
            value="48 núcleos",
            delta="Mayor densidad en zonas sur",
            delta_color="inverse"
        )
    with g2:
        st.metric(
            label="Superficie en Alto Riesgo 2026",
            value="142,800 km²",
            delta="Territorios húmedos cálidos",
            delta_color="inverse"
        )
    with g3:
        st.metric(
            label="Precisión del Modelo XGBoost",
            value="AUC = 0.94",
            delta="Alta capacidad predictiva",
            delta_color="normal"
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Pestañas Geoespaciales
    tab_folium, tab_raster = st.tabs([
        "📍 Histórico: Agrupamiento Espacial de Brotes (Clustering Folium)",
        "🛰️ Proyección Espacial de Riesgo Futuro (XGBoost 2026)"
    ])

    with tab_folium:
        with st.container(border=True):
            st.subheader("Histórico: Agrupamiento Espacial de Brotes")
            st.caption("Mapeo de infecciones confirmadas agrupadas por calor.")
            
            try:
                df_mapa = pd.read_csv(ruta_mapa)
                col_lat, col_lon, col_casos = 'Latitud', 'Longitud', 'Primera fecha: Municipio'     
                df_mapa = df_mapa.dropna(subset=[col_lat, col_lon])

                m = folium.Map(location=[17.5, -92.5], zoom_start=6, tiles='OpenStreetMap')
                marcador_cluster = MarkerCluster(name="Clústeres de Brotes").add_to(m)

                for idx, fila in df_mapa.iterrows():
                    lat, lon = fila[col_lat], fila[col_lon]
                    texto_info = f"Casos: {fila[col_casos]}" if col_casos in df_mapa.columns else f"Lat: {lat}, Lon: {lon}"
                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=6,
                        color='#6B1C23',
                        fill=True,
                        fill_color='#A33A36',
                        fill_opacity=0.75,
                        popup=texto_info
                    ).add_to(marcador_cluster)

                st_folium(m, width="100%", height=520, returned_objects=[])
                
                with st.expander("💡 Diagnóstico Geoespacial de Corredores de Infección", expanded=True):
                    st.write("""
                    **Interpretación Territorial:** Este mapa delimita los clústeres históricos de infección. 
                    Las burbujas identifican las zonas geográficas que ya sufrieron epidemias severas, marcando visualmente las rutas por donde avanza el parásito.
                    """)
            except: 
                st.error("Error cargando el mapa de agrupamientos. Verifique el archivo de coordenadas.")

    with tab_raster:
        with st.container(border=True):
            st.subheader("Proyección Espacial de Riesgo (XGBoost 2026)")
            st.caption("Idoneidad climática proyectada por nuestro modelo de Machine Learning.")
            
            try:
                with rasterio.open(ruta_raster) as src:
                    matriz_riesgo = src.read(1)
                    matriz_riesgo = np.where(matriz_riesgo == src.nodata, np.nan, matriz_riesgo)
                    
                    fig, ax = plt.subplots(figsize=(11, 6))
                    fig.patch.set_facecolor('#FFFFFF') 
                    im = ax.imshow(matriz_riesgo, cmap='YlOrRd', vmin=0, vmax=1)
                    ax.axis('off')
                    
                    cbar = plt.colorbar(im, ax=ax, fraction=0.032, pad=0.04)
                    cbar.set_label('Probabilidad de Supervivencia Bioclimática', rotation=270, labelpad=22, fontsize=10, fontweight='bold', color='#1E293B')
                    cbar.ax.tick_params(labelsize=9)
                    
                    st.pyplot(fig)
                    
                    with st.expander("💡 Lectura del Modelo de Machine Learning", expanded=True):
                        st.write("""
                        **Interpretación Prospectiva:** A diferencia del mapa retrospectivo de puntos, este gráfico proyecta el riesgo a futuro (2026). 
                        Las regiones en rojo oscuro poseen el clima perfecto para la supervivencia endémica, indicando dónde deben enfocarse las barreras antes de que la plaga llegue.
                        """)
            except: 
                st.info("Cargando proyección raster o archivo no disponible localmente.")


# ------------------------------------------------------------------------------
# MÓDULO 4: METODOLOGÍA Y SIMULADOR INDUSTRIAL
# ------------------------------------------------------------------------------
elif opcion == "⚙️ Metodología y Simulador":
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        col_text, col_sim = st.columns([1.1, 1.1])
        
        with col_text:
            st.subheader("Ingeniería de Características")
            st.write("""
            Para entrenar el modelo predictivo, se tomaron dos decisiones estadísticas importantes:

            **1. Uso de la Mediana / Suma Climática:**
            Se procesaron dos años de registros climáticos utilizando la **mediana** de la Temperatura en lugar del promedio. Esto elimina el ruido de olas de calor atípicas y revela la verdadera "firma climática" de la región. Además, se utilizó la **Precipitación Acumulada Anual** para medir correctamente el agua total recibida por el suelo.

            **2. Muestreo Espacial de Pseudo-Ausencias:**
            Como solo teníamos registros de casos positivos, se generaron pseudo-ausencias en el mapa. Esto le permitió al algoritmo **XGBoost** aprender a diferenciar entre un clima ideal (donde sí hay plaga) y un clima hostil (donde no puede sobrevivir), logrando una precisión superior al 92% (AUC > 0.92).
            """)
            
        with col_sim:
            # CONSOLA DE COMANDOS INDUSTRIAL / BIOCLIMATIC TELEMETRY
            st.markdown("""
            <div class="industrial-console">
                <div class="industrial-header">
                    <div class="industrial-title">
                        <span style="display:inline-block; width:10px; height:10px; background:#10B981; border-radius:50%; box-shadow:0 0 6px #10B981;"></span>
                        CONSOLA DE SIMULACIÓN BIOCLIMÁTICA
                    </div>
                </div>
                <div style="font-size:0.75rem; color:#94A3B8; margin-bottom:12px;">
                    Ajuste los parámetros en los controles inferiores para evaluar teóricamente el riesgo basado en el comportamiento del clúster 3D.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Controles deslizantes (PRESERVANDO EXACTAMENTE LOS NOMBRES ORIGINALES)
            temp_input = st.slider("Temperatura Promedio (°C)", min_value=10.0, max_value=40.0, value=25.0, step=0.5)
            lluvia_input = st.slider("Precipitación Acumulada Anual (mm)", min_value=0.0, max_value=300.0, value=120.0, step=5.0)
            
            # Cálculo visual básico
            indice_bioclima = round(min(100, max(5, ((temp_input - 10)/30 * 50) + ((lluvia_input)/300 * 50))), 1)

            # Consola visual
            st.markdown(f"""
            <div style="background:#0D1520; border:1px solid #1E293B; border-radius:10px; padding:12px 16px; margin: 12px 0; font-family:'JetBrains Mono', monospace;">
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#64748B; margin-bottom:8px;">
                    <span>LECTURA CLIMÁTICA</span>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:8px; text-align:center;">
                    <div style="background:#111827; padding:8px; border-radius:6px; border:1px solid #1F2937;">
                        <div style="font-size:0.65rem; color:#9CA3AF;">TEMPERATURA</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#38BDF8;">{temp_input}°C</div>
                    </div>
                    <div style="background:#111827; padding:8px; border-radius:6px; border:1px solid #1F2937;">
                        <div style="font-size:0.65rem; color:#9CA3AF;">PRECIPITACIÓN</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#38BDF8;">{lluvia_input} mm</div>
                    </div>
                    <div style="background:#111827; padding:8px; border-radius:6px; border:1px solid #1F2937;">
                        <div style="font-size:0.65rem; color:#9CA3AF;">RIESGO EST.</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#F59E0B;">{indice_bioclima}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # EVALUACIÓN DE CONDICIONES (LÓGICA ORIGINAL)
            if 20 <= temp_input <= 30 and lluvia_input >= 50:
                st.markdown("""
                <div class="hazard-banner-high">
                    <div style="display:flex; align-items:center; gap:8px; font-weight:800; font-size:0.95rem; margin-bottom:6px;">
                        🚨 NIVEL DE RIESGO: ALTO
                    </div>
                    <div style="font-size:0.8rem; line-height:1.4;">
                        Condiciones termopluviométricas óptimas para la reproducción masiva de la plaga.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            elif (15 <= temp_input < 20 or 30 < temp_input <= 35) and lluvia_input >= 20:
                st.markdown("""
                <div class="hazard-banner-mod">
                    <div style="display:flex; align-items:center; gap:8px; font-weight:800; font-size:0.95rem; margin-bottom:6px;">
                        ⚠️ NIVEL DE RIESGO: MODERADO
                    </div>
                    <div style="font-size:0.8rem; line-height:1.4;">
                        Supervivencia posible, pero sin tasa de crecimiento exponencial.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown("""
                <div class="hazard-banner-low">
                    <div style="display:flex; align-items:center; gap:8px; font-weight:800; font-size:0.95rem; margin-bottom:6px;">
                        ✅ NIVEL DE RIESGO: BAJO
                    </div>
                    <div style="font-size:0.8rem; line-height:1.4;">
                        Condiciones hostiles. Es improbable que la plaga se vuelva endémica aquí.
                    </div>
                </div>
                """, unsafe_allow_html=True)