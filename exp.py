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
 
# Gráfico de radar
st.subheader("📊 Comparación Promedio por Especie")
df_radar = df_filtered.groupby("species").mean().reset_index()
fig_radar = px.line_polar(df_radar, r=df_radar.drop(columns="species").mean(axis=1),
                          theta=["sepal_length", "sepal_width", "petal_length", "petal_width"],
                          line_close=True, color=df_radar["species"], title="Perfil Promedio de Cada Especie")
st.plotly_chart(fig_radar)
 
# Tabla de datos interactiva
st.subheader("📄 Datos Filtrados")
st.dataframe(df_filtered)

st.title( "Visualización del dataset Iris" ... par Karen Juliana Gomez Duran
