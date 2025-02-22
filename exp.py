import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
from PIL import Image
 
# Cargar el dataset
st.title("📊 Tablero Gerencial - Análisis de Iris")
df = sns.load_dataset("iris")

# Gráfico de dispersión interactivo
st.subheader("📈 Relación entre Largo y Ancho de Pétalos")
fig = px.scatter(df, x="petal_length", y="petal_width", color="species", 
                 size="sepal_length", hover_data=["sepal_width"], 
                 title="Distribución de Tamaño de los Pétalos")
st.plotly_chart(fig)

species_list = df["species"].unique()
especie = st.selectbox("Seleccione una especie:", species_list)
df_filtered = df.loc[df["species"]==especie]

species_images = {"setosa": "setosa.png",
    "versicolor": "versicolor.png",
    "virginica": "virginica.png"}
 
stats = df_filtered.describe().loc[["mean", "std"]]
image_path = species_images[especie]
image = Image.open(image_path)
col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])  # Imagen en el centro

with col1:
    st.subheader("📏 Sépalos")
    st.write(f"**Largo:** {stats.loc['mean', 'sepal_length']:.2f} ± {stats.loc['std', 'sepal_length']:.2f}")
    st.write(f"**Ancho:** {stats.loc['mean', 'sepal_width']:.2f} ± {stats.loc['std', 'sepal_width']:.2f}")

with col3:
    st.image(image, caption=f"Flor Iris - {selected_species.capitalize()}", use_container_width=True)
 
with col5:
    st.subheader("🌺 Pétalos")
    st.write(f"**Largo:** {stats.loc['mean', 'petal_length']:.2f} ± {stats.loc['std', 'petal_length']:.2f}")
    st.write(f"**Ancho:** {stats.loc['mean', 'petal_width']:.2f} ± {stats.loc['std', 'petal_width']:.2f}")
 
# KPIs
st.subheader("📌 Métricas Clave")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🌱 Número de Registros", value=df_filtered.shape[0])
with col2:
    st.metric(label="🌿 Promedio Sepal Length", value=round(df_filtered["sepal_length"].mean(), 2))
with col3:
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

st.title("Visualización del dataset Iris")

st.subheader("📄 Datos Filtrados")
st.dataframe(df_filtered)

st.write("### Boxplot de Sepal Length y Sepal Width para la Especie Seleccionada")
col1, col2 = st.columns(2)
with col1:
 fig1 = px.box(df_filtered, y="sepal_length", title="Sepal Length")
 st.plotly_chart(fig1)
 fig4 = px.box(df_filtered, y="petal_length", title="Petal Length")
 st.plotly_chart(fig4)

with col2:
  fig2 = px.box(df_filtered, y="sepal_width", title="Sepal Width")
  st.plotly_chart(fig2)
  fig3 = px.box(df_filtered, y="petal_width", title="Petal Width")
  st.plotly_chart(fig3)
