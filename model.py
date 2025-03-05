import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 🎨 Estilo de la app
st.set_page_config(page_title="Calculadora de Tarifas", layout="centered", page_icon="🚛")

st.markdown("""
    <style>
    .stApp {background-color: #f8f9fa;}
    .title {color: #2c3e50; text-align: center;}
    .subtitle {color: #7f8c8d; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# 🔹 Simulación de datos (reemplazar con modelo real)
def calcular_tarifa(origen, destino, tipo_camion):
    base_rate = np.random.uniform(1.5, 2.5)  # Tarifa base por milla ($)
    distancia = np.random.uniform(200, 1500)  # Distancia simulada (millas)
    
    # Ajuste por tipo de camión
    factor_camion = {"Seco": 1.0, "Refrigerado": 1.2, "Plataforma": 1.15}
    multiplicador = factor_camion.get(tipo_camion, 1.0)
    
    tarifa_promedio = base_rate * distancia * multiplicador
    tarifa_inferior = tarifa_promedio * 0.85
    tarifa_superior = tarifa_promedio * 1.15

    return distancia, tarifa_inferior, tarifa_promedio, tarifa_superior

# 🔹 Encabezado
st.markdown("<h1 class='title'>🚚 Calculadora de Tarifas de Carga</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Ingresa los datos para estimar el costo del flete</p>", unsafe_allow_html=True)

# 🔹 Entrada de datos
col1, col2 = st.columns(2)
origen = col1.selectbox("📍 Origen", ["Los Ángeles", "Nueva York", "Houston", "Chicago", "Miami"])
destino = col2.selectbox("📍 Destino", ["Dallas", "Atlanta", "Seattle", "Denver", "San Francisco"])
tipo_camion = st.radio("🚛 Tipo de Camión", ["Seco", "Refrigerado", "Plataforma"])

# 🔹 Calcular tarifa
if st.button("Calcular Tarifa"):
    distancia, tarifa_min, tarifa_media, tarifa_max = calcular_tarifa(origen, destino, tipo_camion)

    # 🔹 Mostrar resultados
    st.success(f"📏 Distancia estimada: **{distancia:.0f} millas**")
    st.info(f"💲 Intervalo de tarifa esperado:")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Inferior", f"${tarifa_min:,.2f}")
    col2.metric("Promedio", f"${tarifa_media:,.2f}")
    col3.metric("Superior", f"${tarifa_max:,.2f}")

    # 🔹 Gráfico interactivo con Plotly
    df_tarifas = pd.DataFrame({
        "Categoría": ["Inferior", "Promedio", "Superior"],
        "Tarifa": [tarifa_min, tarifa_media, tarifa_max]
    })

    fig = px.bar(df_tarifas, x="Categoría", y="Tarifa", text="Tarifa",
                 color="Categoría", color_discrete_sequence=["#27ae60", "#2980b9", "#c0392b"],
                 title="📊 Rango de Tarifas Estimadas")
    
    fig.update_traces(texttemplate="$%{text:,.2f}", textposition="outside")
    fig.update_layout(yaxis_title="Tarifa ($)", xaxis_title="",
                      plot_bgcolor="#ecf0f1", margin=dict(l=40, r=40, t=40, b=40))

    st.plotly_chart(fig, use_container_width=True)
