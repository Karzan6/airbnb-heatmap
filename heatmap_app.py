import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Title of the app
st.title("Airbnb Heatmap for London")

# Load data
@st.cache_data
def load_data():
    # Replace the URL with your online CSV file or local file path
    url = "https://path_to_your_online_dataset.csv"
    try:
        data = pd.read_csv(url)
    except Exception as e:
        st.error("Error loading data. Please check your URL.")
        st.write(e)
        return None
    return data

data = load_data()

if data is not None:
    # Ensure valid latitude and longitude data
    data = data.dropna(subset=['latitude', 'longitude'])
    
    # Sidebar filters
    price_min, price_max = st.sidebar.slider("Price Range (£)", 0, int(data['price'].max()), (0, 500))
    data = data[(data['price'] >= price_min) & (data['price'] <= price_max)]
    
    # Generate the map
    m = folium.Map(location=[51.509865, -0.118092], zoom_start=10)  # Centered on London
    HeatMap(data[['latitude', 'longitude']].values, radius=8, blur=6).add_to(m)
    
    # Display the map
    st_folium(m, width=700, height=500)

