import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

# Page configuration
st.set_page_config(page_title="Freight Rate Calculator", layout="wide", page_icon="🚛")

# Styling
st.markdown("""
    <style>
    .stApp {background-color: #adbee5; color: white;}
    .title {color: #00ccff; text-align: center; font-size: 32px;}
    .subtitle {color: #cccccc; text-align: center; font-size: 18px;}
    </style>
    """, unsafe_allow_html=True)

# Styling
title_html = """
    <h1 style='text-align: center; color: #527bd9;'>Find a load for your truck</h1>
    <p style='text-align: center; color: #333;'>Add the origin, destination, and trailer type, then click Search to find loads for you.</p>
"""
st.markdown(title_html, unsafe_allow_html=True)

# Simulated Data
np.random.seed(42)
data = {
    "city_origin": np.random.choice(["Los Angeles", "New York", "Houston", "Chicago", "Miami"], 100),
    "city_destination": np.random.choice(["Dallas", "Atlanta", "Seattle", "Denver", "San Francisco"], 100),
    "state_origin": np.random.choice(["CA", "NY", "TX", "IL", "FL"], 100),
    "state_destination": np.random.choice(["TX", "GA", "WA", "CO", "CA"], 100),
    "pickup_date": pd.date_range(start="2024-01-01", periods=100, freq='D'),
    "dropoff_date": pd.date_range(start="2024-01-02", periods=100, freq='D'),
    "age": np.random.randint(1, 30, 100),
    "rate": np.random.uniform(500, 5000, 100),
    "distance": np.random.uniform(200, 1500, 100),
    "trailer": np.random.choice(["Flatbed", "Reefer", "Van"], 100),
    "size": np.random.choice(["Full", "Partial"], 100),
    "weight": np.random.randint(5000, 45000, 100)
}
df = pd.DataFrame(data)

# Unique city pairs
df["lane"] = df["city_origin"] + " ➝ " + df["city_destination"]
lanes = df["lane"].unique()

# User Inputs
col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
selected_origin = col1.selectbox("Select origin", df["city_origin"].unique())
selected_destination = col2.selectbox("Select destination", df["city_destination"].unique())
selected_trailer = col3.selectbox("Trailer Type", df["trailer"].unique())

with col4:
    st.markdown("<br>", unsafe_allow_html=True)  # Añade más espacio vertical
    search_btn = st.button("Search", use_container_width=True)  # Hace que el botón ocupe todo el ancho

# CSS para evitar hover en el botón
st.markdown("""
    <style>
    div[data-testid="stButton"] button {
        background-color: #527bd9;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
        border: none;
        transition: none;
    }
    /* Color cuando se hace hover */
    div[data-testid="stButton"] button:hover {
        background-color: #0747d9;
        color: white;
    }
    
    /* Color cuando se presiona */
    div[data-testid="stButton"] button:active {
        background-color: #527bd9;
        color: white;
    
    }
    </style>
    """, unsafe_allow_html=True)

selected_lane = (selected_origin +  " ➝ " + selected_destination)

if search_btn:
    filtered_df = df[(df["lane"] == selected_lane) & (df["trailer"] == selected_trailer)]
    
    if not filtered_df.empty:
        colA, colB = st.columns([4, 1])
        colA.success(f"🔍 Found **{len(filtered_df)}** loads for this lane.")
        
        with colB:
            with st.expander("🌟 Rate Evaluation"):
                st.write("### Rate Category")
                st.image("image.png", use_column_width=True)
                
        filtered_df["details"] = filtered_df["reference_id"].astype(str) + " | Click for details"
        selected_row = st.selectbox("Select a load to view details", filtered_df["details"])
        
        if selected_row:
            load_details = filtered_df[filtered_df["details"] == selected_row].iloc[0]
            
            with st.expander("📅 View Load Details"):
                st.write(f"**Reference ID:** {load_details['reference_id']}")
                st.write(f"**Contact Info:** +1-800-LOAD-INFO")
                
                origin_coords = (34.0522, -118.2437)
                destination_coords = (32.7767, -96.7970)
                map_ = folium.Map(location=origin_coords, zoom_start=5)
                folium.Marker(origin_coords, popup="Origin", icon=folium.Icon(color="blue")).add_to(map_)
                folium.Marker(destination_coords, popup="Destination", icon=folium.Icon(color="red")).add_to(map_)
                folium_static(map_)
    else:
        st.warning("⚠️ No loads available for this selection.")
