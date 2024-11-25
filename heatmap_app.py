import pandas as pd
import folium
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import st_folium

# Load the Airbnb listings dataset
@st.cache_data
def load_data():
    url = "https://data.insideairbnb.com/united-kingdom/england/london/2024-09-06/visualisations/listings.csv"
    df = pd.read_csv(url)
    return df

# Preprocess the data
def preprocess_data(df):
    df = df.dropna(subset=['latitude', 'longitude', 'price'])  # Drop rows with missing data
    df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Ensure price is numeric
    return df

# Generate the heatmap
def create_heatmap(df):
    # Create a map centered on London
    heatmap = folium.Map(location=[51.5074, -0.1278], zoom_start=10)

    # Add heatmap layer
    heat_data = [[row['latitude'], row['longitude'], row['price']] for _, row in df.iterrows()]
    HeatMap(heat_data, radius=10).add_to(heatmap)

    return heatmap

# Streamlit app
st.title("London Airbnb Heatmap")

st.markdown("""
This app visualizes Airbnb listings in London using a heatmap. The dataset is from the 
[Inside Airbnb project](http://insideairbnb.com/).
""")

# Load and preprocess the data
st.write("Loading data...")
data = load_data()
processed_data = preprocess_data(data)
st.write("Data loaded and processed.")

# Display heatmap
st.write("Generating heatmap...")
map_object = create_heatmap(processed_data)
st_folium(map_object, width=700, height=500)

st.success("Heatmap created!")
