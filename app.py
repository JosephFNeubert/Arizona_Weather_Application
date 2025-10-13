"""
File: App.py
Author: Joseph Neubert
Description: Application frontend deriving data from city weather JSON files produced by ArizonaWeatherFetch.py. This app uses the
Streamlit module for display and deployment of a webpage, and it is able to run the backend script as a subprocess upon user input.
The webpage banner image was royalty-free and altered by me to include the overlayed text.
"""

# IMPORTS
import streamlit as st
import json
import subprocess
import pandas as pd
from PIL import Image
from ArizonaWeatherFetch import cities_tuple

data = {}


# FUNCTION DEFINITIONS
def generate_data() -> None:
    """Subprocess to run backend file to update JSON files"""
    subprocess.run(["python", "ArizonaWeatherFetch.py"])


def display_data(city: str) -> None:
    """
    Graphically generate data
    TODO: Create an aesthetically pleasing template for this function to execute instead of a JSON dump
    TODO: Add new elif statements in accordance with the number of cities added
    """
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


# FRONTEND DISPLAY
banner = Image.open("Assets/Banner.png")
st.image(banner, use_container_width=True)
st.text("Please select a city to view its weather conditions.")
city_select = st.selectbox("Select city", ["Phoenix", "Prescott"])
if st.button("Load Data"):
    display_data(city_select)
