import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 🎨 Estilo de la app
st.set_page_config(page_title="Calculadora de Tarifas", layout="centered", page_icon="🚛")

st.markdown("""
    <style>
    .stApp {background-color: #f8f9fa;}
    .title {color: #2c3e50; text-align: center;}
    .subtitle {color: #7f8c8d; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# 🔹 Simulación de datos de cargas (Reemplazar con datos reales)
data = {
    "load_id": np.arange(1, 101),
    "origen": np.random.choice(["Los Ángeles", "Nueva York", "Houston", "Chicago", "Miami"], 100),
    "destino": np.random.choice(["Dallas", "Atlanta", "Seattle", "Denver", "San Francisco"], 100),
    "tipo_camion": np.random.choice(["Flatbed", "Reefer", "Van"], 100),
    "tarifa": np.random.uniform(500, 5000, 100)  # Tarifas en dólares
}
df_cargas = pd.DataFrame(data)

# 🔹 Función para calcular la tarifa esperada
def calcular_tarifa(origen, destino, tipo_camion):
    base_rate = np.random.uniform(1.5, 2.5)  # Tarifa base por milla ($)
    distancia = np.random.uniform(200, 1500)  # Distancia simulada (millas)

    # Ajuste por tipo de camión
    factor_camion = {"Flatbed": 1.0, "Reefer": 1.2, "Van": 1.15}
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
origen = col1.selectbox("📍 Origen", df_cargas["origen"].unique())
destino = col2.selectbox("📍 Destino", df_cargas["destino"].unique())
tipo_camion = st.radio("🚛 Tipo de Camión", ["Seco", "Refrigerado", "Plataforma"])

# 🔹 Calcular tarifa
if st.button("Calcular Tarifa"):
    distancia, tarifa_min, tarifa_media, tarifa_max = calcular_tarifa(origen, destino, tipo_camion)

    st.success(f"📏 Distancia estimada: **{distancia:.0f} millas**")
    st.info(f"💲 Intervalo de tarifa esperado:")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Inferior", f"${tarifa_min:,.2f}")
    col2.metric("Promedio", f"${tarifa_media:,.2f}")
    col3.metric("Superior", f"${tarifa_max:,.2f}")
    
    # 🔹 Barra de intervalo interactiva
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=tarifa_media,
        title={"text": "Tarifa Estimada ($)"},
        gauge={
            "axis": {"range": [tarifa_min * 0.9, tarifa_max * 1.1]},
            "bar": {"color": "blue"},
            "steps": [
                {"range": [tarifa_min, tarifa_max], "color": "lightblue"}
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    # 🔹 Filtrar cargas según los parámetros seleccionados
    df_filtrado = df_cargas[
        (df_cargas["origen"] == origen) &
        (df_cargas["destino"] == destino) &
        (df_cargas["tipo_camion"] == tipo_camion)
    ]

    if not df_filtrado.empty:
        st.success(f"🔍 Se encontraron **{len(df_filtrado)}** cargas con estos parámetros:")
        st.dataframe(df_filtrado[["load_id", "tarifa"]].rename(columns={"load_id": "ID de Carga", "tarifa": "Tarifa ($)"}))
    else:
        st.warning("⚠️ No hay cargas disponibles con estos parámetros.")
