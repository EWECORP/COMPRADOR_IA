import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# Generar datos simulados
def generar_datos():
    fechas = pd.date_range(start="2024-01-01", periods=12, freq="M")
    categorias = ["Abarrotes", "Bebidas", "Lácteos", "Perecederos"]
    datos = {
        "Fecha": np.tile(fechas, len(categorias)),
        "Categoría": np.repeat(categorias, len(fechas)),
        "Facturación": np.random.randint(500000, 1000000, len(fechas) * len(categorias)),
        "Consumo Promedio Diario": np.random.uniform(100, 500, len(fechas) * len(categorias)),
        "Stock Actual (Días)": np.random.uniform(10, 50, len(fechas) * len(categorias)),
        "Órdenes Pendientes": np.random.randint(0, 20, len(fechas) * len(categorias)),
        "OTIF (%)": np.random.uniform(80, 100, len(fechas) * len(categorias)),
        "Stock Crítico": np.random.randint(0, 10, len(fechas) * len(categorias)),
        "Sobrestock": np.random.uniform(0, 100, len(fechas) * len(categorias)),
        "Faltantes de Stock": np.random.randint(0, 15, len(fechas) * len(categorias)),
        "Margen Bruto (%)": np.random.uniform(10, 40, len(fechas) * len(categorias)),
        "Quiebre de Stock (%)": np.random.uniform(2, 8, len(fechas) * len(categorias)),
    }
    df = pd.DataFrame(datos)
    df["Fecha"] = pd.to_datetime(df["Fecha"])  # Asegurarse de que las fechas sean tipo datetime
    return pd.DataFrame(datos)

df = generar_datos()

# Configuración del tablero
st.set_page_config(layout="wide", page_title="Tablero Gerencial DIARCO")

# Títulos
st.title("Tablero Gerencial - Compras y Ventas")
st.markdown("Este tablero muestra indicadores clave para el análisis de Compras y Ventas en DIARCO.")

# Filtros
st.sidebar.header("Filtros")
categoria_seleccionada = st.sidebar.selectbox("Seleccione Categoría", df["Categoría"].unique())
fecha_seleccionada = st.sidebar.slider(
    "Rango de Fechas",
    min_value=df["Fecha"].min().to_pydatetime(),
    max_value=df["Fecha"].max().to_pydatetime(),
    value=(df["Fecha"].min().to_pydatetime(), df["Fecha"].max().to_pydatetime()),
)

# Filtrar datos
datos_filtrados = df[
    (df["Categoría"] == categoria_seleccionada) &
    (df["Fecha"] >= fecha_seleccionada[0]) &
    (df["Fecha"] <= fecha_seleccionada[1])
]

# Indicadores Clave
st.header("Indicadores Clave")
col1, col2, col3, col4 = st.columns(4)

with col1:
    cobertura_stock = datos_filtrados["Stock Actual (Días)"].mean()
    st.metric(label="Cobertura de Stock (Días)", value=f"{cobertura_stock:.2f}")

with col2:
    ordenes_pendientes = datos_filtrados["Órdenes Pendientes"].sum()
    st.metric(label="Órdenes Pendientes", value=f"{ordenes_pendientes}")

with col3:
    otif_promedio = datos_filtrados["OTIF (%)"].mean()
    st.metric(label="Cumplimiento de Proveedores (OTIF)", value=f"{otif_promedio:.2f}%")

with col4:
    stock_critico = datos_filtrados["Stock Crítico"].sum()
    st.metric(label="Alertas de Stock Crítico", value=f"{stock_critico}")

#Indicadores Sugeridos
st.header("Indicadores Sugeridos")
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

# Cobertura de Stock
fig1 = px.line(
    datos_filtrados,
    x="Fecha",
    y="Stock Actual (Días)",
    title="Cobertura de Stock en Días",
    markers=True,
    labels={"Stock Actual (Días)": "Cobertura (Días)", "Fecha": "Mes"}
)
st.plotly_chart(fig1, use_container_width=True)

# Sobrestock por Campañas
fig2 = px.bar(
    datos_filtrados,
    x="Fecha",
    y="Sobrestock",
    title="Sobrestock por Campañas",
    labels={"Sobrestock": "Exceso de Stock", "Fecha": "Mes"}
)
st.plotly_chart(fig2, use_container_width=True)

# Faltantes de Stock
fig3 = px.bar(
    datos_filtrados,
    x="Fecha",
    y="Faltantes de Stock",
    title="Faltantes de Stock por Mes",
    labels={"Faltantes de Stock": "Productos Faltantes", "Fecha": "Mes"}
)
st.plotly_chart(fig3, use_container_width=True)

# Indicadores Sugeridos
st.header("Indicadores Sugeridos")

col1, col2 = st.columns(2)

with col1:
    ventas_categoria = datos_filtrados.groupby("Fecha")["Facturación"].sum()
    fig4 = px.line(
        ventas_categoria,
        x=ventas_categoria.index,
        y=ventas_categoria.values,
        title="Evolución de Ventas por Categoría",
        markers=True,
        labels={"x": "Mes", "y": "Facturación"}
    )
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    eficiencia_algoritmo = np.random.uniform(70, 95)
    st.metric(label="Eficiencia en Uso del Algoritmo", value=f"{eficiencia_algoritmo:.2f}%")

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

# Comentarios adicionales
st.sidebar.markdown("## Metas")
st.sidebar.text("Facturación: $800,000 por mes")
st.sidebar.text("Margen Bruto: 25% promedio")
st.sidebar.text("Quiebre de Stock: Máximo 3%")

# Footer
st.markdown("Desarrollado por el equipo de sistemas.")
