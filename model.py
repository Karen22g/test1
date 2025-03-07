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
    # Filter Data
    filtered_df = df[(df["lane"] == selected_lane) & (df["trailer"] == selected_trailer)]
    
    if not filtered_df.empty:
        st.success(f"🔍 Found **{len(filtered_df)}** loads for this lane.")
        
        # Table Display
        filtered_df["specifications"] = filtered_df["size"] + " | " + filtered_df["weight"].astype(str) + " lbs"
        st.dataframe(filtered_df[["city_origin", "state_origin", "city_destination", "state_destination", "pickup_date", "dropoff_date", "age", "rate", "distance", "trailer", "specifications"]].rename(columns={
            "city_origin": "Origin City",
            "state_origin": "Origin State",
            "city_destination": "Destination City",
            "state_destination": "Destination State",
            "pickup_date": "Pickup Date",
            "dropoff_date": "Dropoff Date",
            "age": "Age (days)",
            "rate": "Rate ($)",
            "distance": "Distance (miles)",
            "trailer": "Trailer Type",
            "specifications": "Specifications"
        }))
        
        # Lane Rate Evaluation
        y_predicted = filtered_df["rate"].mean()
        mad = 50
        
        def categorize_rate(rate):
            if rate < (y_predicted - mad):
                return "🔴 Red (Low)"
            elif rate < y_predicted:
                return "🟠 Orange (Below Avg)"
            elif rate < (y_predicted + mad):
                return "🟡 Yellow (Above Avg)"
            else:
                return "🟢 Green (High)"
        
        filtered_df["Rate Category"] = filtered_df["rate"].apply(categorize_rate)
        st.write("### Lane Rate Evaluation")
        st.dataframe(filtered_df[["rate", "Rate Category"]].rename(columns={"rate": "Rate ($)"}))
        
        # Map Visualization
        st.write("### Load Details on Map")
        origin_coords = (34.0522, -118.2437)  # Placeholder for geolocation data
        destination_coords = (32.7767, -96.7970)
        
        map_ = folium.Map(location=origin_coords, zoom_start=5)
        folium.Marker(origin_coords, popup="Origin", icon=folium.Icon(color="blue")).add_to(map_)
        folium.Marker(destination_coords, popup="Destination", icon=folium.Icon(color="red")).add_to(map_)
        folium_static(map_)
    else:
        st.warning("⚠️ No loads available for this selection.")
