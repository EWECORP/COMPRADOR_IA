import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime

# Generar datos simulados
def generar_datos():
    fechas = pd.date_range(start="2024-01-01", periods=12, freq="M")
    categorias = ["Abarrotes", "Bebidas", "Lácteos", "Perecederos"]
    datos = {
        "Fecha": np.tile(fechas, len(categorias)),
        "Categoría": np.repeat(categorias, len(fechas)),
        "Facturación": np.random.randint(500000, 1000000, len(fechas) * len(categorias)),
        "Margen Bruto (%)": np.random.uniform(10, 40, len(fechas) * len(categorias)),
        "Quiebre de Stock (%)": np.random.uniform(2, 8, len(fechas) * len(categorias)),
    }
    df = pd.DataFrame(datos)
    df["Fecha"] = pd.to_datetime(df["Fecha"])  # Asegurarse de que las fechas sean tipo datetime
    return df

df = generar_datos()

# Configuración del tablero
st.set_page_config(layout="wide", page_title="Tablero Gerencial DIARCO")

# Títulos
st.title("Tablero Gerencial - Compras y Ventas")
st.markdown("Este tablero muestra indicadores clave para el análisis de Compras y Ventas en DIARCO.")

# Filtros
st.sidebar.header("Filtros")
categoria_seleccionada = st.sidebar.selectbox("Seleccione Categoría", df["Categoría"].unique())

# Convertir las fechas a datetime para evitar errores
fecha_min = df["Fecha"].min().to_pydatetime()
fecha_max = df["Fecha"].max().to_pydatetime()

fecha_seleccionada = st.sidebar.slider(
    "Rango de Fechas", 
    min_value=fecha_min, 
    max_value=fecha_max, 
    value=(fecha_min, fecha_max)
)

# Filtrar datos
datos_filtrados = df[
    (df["Categoría"] == categoria_seleccionada) & 
    (df["Fecha"] >= fecha_seleccionada[0]) & 
    (df["Fecha"] <= fecha_seleccionada[1])
]

# Indicadores Clave
st.header("Indicadores Clave")
col1, col2, col3 = st.columns(3)

with col1:
    facturacion_total = datos_filtrados["Facturación"].sum()
    st.metric(label="Facturación Total ($)", value=f"${facturacion_total:,.2f}")

with col2:
    margen_promedio = datos_filtrados["Margen Bruto (%)"].mean()
    st.metric(label="Margen Bruto Promedio (%)", value=f"{margen_promedio:.2f}%")

with col3:
    quiebre_promedio = datos_filtrados["Quiebre de Stock (%)"].mean()
    st.metric(label="Quiebre de Stock Promedio (%)", value=f"{quiebre_promedio:.2f}%")

# Gráficos
st.header("Evolución de Indicadores")

# Facturación por Mes
fig1 = px.line(
    datos_filtrados, 
    x="Fecha", 
    y="Facturación", 
    title="Evolución de la Facturación",
    markers=True,
    labels={"Facturación": "Facturación ($)", "Fecha": "Mes"},
)
st.plotly_chart(fig1, use_container_width=True)

# Margen Bruto por Mes
fig2, ax = plt.subplots()
datos_filtrados.groupby("Fecha")["Margen Bruto (%)"].mean().plot(ax=ax, marker='o', color='green')
ax.axhline(y=margen_promedio, color='red', linestyle='--', label='Meta')
ax.set_title("Margen Bruto Promedio por Mes")
ax.set_xlabel("Mes")
ax.set_ylabel("Margen Bruto (%)")
ax.legend()
st.pyplot(fig2)

# Quiebre de Stock
fig3 = px.bar(
    datos_filtrados, 
    x="Fecha", 
    y="Quiebre de Stock (%)", 
    title="Quiebre de Stock Mensual",
    labels={"Quiebre de Stock (%)": "Quiebre de Stock (%)", "Fecha": "Mes"},
)
st.plotly_chart(fig3, use_container_width=True)

# Comentarios adicionales
st.sidebar.markdown("## Metas")
st.sidebar.text("Facturación: $800,000 por mes")
st.sidebar.text("Margen Bruto: 25% promedio")
st.sidebar.text("Quiebre de Stock: Máximo 3%")

# Footer
st.markdown("Desarrollado por el equipo de sistemas.")
