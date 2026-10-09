# 🪰 Modelado de Nicho Ecológico: Gusano Barrenador del Ganado (GBG)

## 📌 Descripción del Proyecto
Sistema de inteligencia geoespacial y epidemiológica para proyectar el riesgo de propagación del Gusano Barrenador del Ganado (*Cochliomyia hominivorax*) en México y Centroamérica. El proyecto integra análisis climático histórico, clustering de brotes y un motor predictivo basado en Machine Learning espacial.

## ⚙️ Arquitectura Técnica
*   **Procesamiento Geospacial:** Extracción de firmas bioclimáticas mediante `rasterio` y `elapid` sobre tensores climáticos continuos.
*   **Machine Learning (XGBoost):** Entrenamiento de clasificación binaria (Presencia vs. Pseudo-ausencias) para delimitar el Nicho Ecológico Fundamental (AUC > 0.92).
*   **Data Visualization:** Dashboards interactivos desarrollados con `Plotly` y agrupamiento georreferenciado con `Folium`.
*   **Despliegue Web:** Interfaz analítica reactiva construida nativamente en `Streamlit`.

## 📁 Estructura del Repositorio
*   `/data/` - Matrices CSV, Rusters (.tif) y datos climáticos procesados.
*   `/notebooks/` - Jupyter Notebooks con el pipeline de limpieza, EDA y entrenamiento espacial, junto con la aplicación principal `app.py`.
*   `/src/` - Scripts de soporte y módulos auxiliares.

## 🚀 Ejecución Local
Para visualizar el Monitor Epidemiológico en tu máquina local:
1. Clona este repositorio.
2. Instala las dependencias: `pip install -r notebooks/requirements.txt`
3. Inicia el servidor: `streamlit run notebooks/app.py`

## Página web
* link: https://monitor-gusano-barrenador-e8qfvbmcyzjzmizjtppbvd.streamlit.app/
---

*Desarrollado por Moises Segura Carrillo - Facultad de Ciencias Físico-Matemáticas (BUAP).*
