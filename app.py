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

# CONSTANT
METERS_TO_FEET_CONVERSION = 3.28084

# Declared data dictionary to be loaded by JSON file
data = {}


# FUNCTION DEFINITIONS
def generate_data() -> None:
    """Subprocess to run backend file to update JSON files."""
    subprocess.run(["python", "ArizonaWeatherFetch.py"])


def display_data(city: str) -> None:
    """Load and display data from JSON files with various stylized text fields."""
    # Select city JSON file
    #
    # Add new cities to if block here
    #
    generate_data()
    if city == "Phoenix":
        with open(cities_tuple[0], "r") as f:
            data = json.load(f)

    elif city == "Prescott":
        with open(cities_tuple[1], "r") as f:
            data = json.load(f)

    elif city == "Flagstaff":
        with open(cities_tuple[2], "r") as f:
            data = json.load(f)

    elif city == "Tucson":
        with open(cities_tuple[3], "r") as f:
            data = json.load(f)

    elif city == "Sedona":
        with open(cities_tuple[4], "r") as f:
            data = json.load(f)

    elif city == "Payson":
        with open(cities_tuple[5], "r") as f:
            data = json.load(f)

    elif city == "Page":
        with open(cities_tuple[6], "r") as f:
            data = json.load(f)

    elif city == "Yuma":
        with open(cities_tuple[7], "r") as f:
            data = json.load(f)

    elif city == "Lake Havasu City":
        with open(cities_tuple[8], "r") as f:
            data = json.load(f)

    elif city == "Casa Grande":
        with open(cities_tuple[9], "r") as f:
            data = json.load(f)

    else:
        st.text("ERROR: Unable to generate weather data. Try again later...")

    # Display all data as text fields
    st.header(f"{city.upper()} WEATHER", divider="orange")
    st.subheader(":world_map: Location Details")
    st.text(f"Latitude: {data.get('latitude')}")
    st.text(f"Longitude: {data.get('longitude')}")
    st.text(
        f"Elevation: {round(data.get('elevation') * METERS_TO_FEET_CONVERSION, 2)} feet"
    )
    st.text("")
    st.subheader(":partly_sunny: Current Weather")
    st.text(f"Current Temperature: {round(data.get('currentTemperature'))}°F")
    st.text(f"Current Humidity: {round(data.get('currentHumidity'))}%")
    st.text(f"Current Precipitation: {round(data.get('currentPrecipitation'))} inches")
    st.text("")
    st.subheader(f":clock3: Hourly Weather")
    st.text("Temperatures, Humidities, Precipitations, Precipitation Probabilities")
    for interval in data.get("hourlyTimeIntervals"):
        curr_index = (data.get("hourlyTimeIntervals")).index(interval)
        st.text(
            f"{pd.to_datetime(interval, unit='s')}  —  {round(data.get('hourlyTemperatures')[curr_index])}°F,   {round(data.get('hourlyHumidities')[curr_index])}% humidity,   {round(data.get('hourlyPrecipitations')[curr_index], 3)} inches of precipitation,   {round(data.get('hourlyPrecipitationProbabilities')[curr_index])}% precipitation probability"
        )


# FRONTEND DISPLAY
banner = Image.open("Assets/Banner.png")
city_list = [
    "Phoenix",
    "Prescott",
    "Flagstaff",
    "Tucson",
    "Sedona",
    "Payson",
    "Page",
    "Yuma",
    "Lake Havasu City",
    "Casa Grande",
]
st.image(banner, use_container_width=True)
st.text("Please select a city to view its weather conditions.")
city_select = st.selectbox("Select city", sorted(city_list))
if st.button("Load Data"):
    display_data(city_select)
