import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
 
# Cargar el dataset
st.title("📊 Tablero Gerencial - Análisis de Iris")
df = sns.load_dataset("iris")
 
# Sidebar con filtros
st.sidebar.header("Filtros")
especie = st.sidebar.multiselect("Selecciona la especie", df["species"].unique(), default=df["species"].unique())
 
df_filtered = df[df["species"].isin(especie)]
 
# KPIs
st.subheader("📌 Métricas Clave")
st.metric(label="🌱 Número de Registros", value=df_filtered.shape[0])
st.metric(label="🌿 Promedio Sepal Length", value=round(df_filtered["sepal_length"].mean(), 2))
st.metric(label="🌸 Promedio Petal Width", value=round(df_filtered["petal_width"].mean(), 2))
 
# Gráfico de dispersión interactivo
st.subheader("📈 Relación entre Largo y Ancho de Pétalos")
fig = px.scatter(df_filtered, x="petal_length", y="petal_width", color="species", 
                 size="sepal_length", hover_data=["sepal_width"], 
                 title="Distribución de Tamaño de los Pétalos")
st.plotly_chart(fig)

# Calcular el promedio de cada especie
st.subheader("📊 Comparación Promedio por Especie")
df_radar = df_filtered.groupby("species").mean().reset_index()

# Reestructurar los datos para Plotly
df_melted = df_radar.melt(id_vars=["species"], var_name="Feature", value_name="Value")

# Crear el gráfico de radar
fig_radar = px.line_polar(df_melted, r="Value", theta="Feature", 
                          color="species", line_close=True, 
                          title="Perfil Promedio de Cada Especie")

st.plotly_chart(fig_radar)
 
# Tabla de datos interactiva
st.subheader("📄 Datos Filtrados")
st.dataframe(df_filtered)
