# IMPORTS
import streamlit as st
import json
import subprocess
import pandas as pd
from PIL import Image
from ArizonaWeatherFetch import cities_tuple

data = {}


# Subprocess to run backend file to update JSON files
def generate_data() -> None:
    subprocess.run(["python", "ArizonaWeatherFetch.py"])


# Graphically generate data
def display_data(city: str) -> None:
    if city == "Phoenix":
        generate_data()
        with open(cities_tuple[0], "r") as f:
            data = json.load(f)
        st.json(data)
    elif city == "Prescott":
        generate_data()
        with open(cities_tuple[1], "r") as f:
            data = json.load(f)
        st.json(data)
    else:
        st.text("Unable to generate weather data. Try again later...")


# Frontend
banner = Image.open("Assets/Banner.png")
st.image(banner, use_container_width=True)
st.text("Please select a city to view its weather conditions.")
city_select = st.selectbox("Select city", ["Phoenix", "Prescott"])
if st.button("Load Data"):
    display_data(city_select)
