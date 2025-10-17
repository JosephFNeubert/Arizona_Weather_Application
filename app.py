"""
File: App.py
Author: Joseph Neubert
Description: Application frontend deriving data from a city weather list of hash maps produced by ArizonaWeatherFetch.py. This app uses
the Streamlit module for display and deployment of a webpage, and it is able to run the principal backend function upon user input.
The webpage banner image was royalty-free and altered by me to include the overlayed text.
"""

# IMPORTS
import streamlit as st
import pandas as pd
from PIL import Image
import ArizonaWeatherFetch
from ArizonaWeatherFetch import weather_fetch

# CONSTANT
METERS_TO_FEET_CONVERSION = 3.28084

# Declared data dictionary to be loaded by backend
data = {}


def display_data(city: str) -> None:
    """
    Load and display data from JSON files with various stylized text fields.
    """
    #
    # Add new cities to if block here
    #
    if city == "Phoenix":
        data = weather_fetch(0)

    elif city == "Prescott":
        data = weather_fetch(1)

    elif city == "Flagstaff":
        data = weather_fetch(2)

    elif city == "Tucson":
        data = weather_fetch(3)

    elif city == "Sedona":
        data = weather_fetch(4)

    elif city == "Payson":
        data = weather_fetch(5)

    elif city == "Page":
        data = weather_fetch(6)

    elif city == "Yuma":
        data = weather_fetch(7)

    elif city == "Lake Havasu City":
        data = weather_fetch(8)

    elif city == "Casa Grande":
        data = weather_fetch(9)

    else:
        st.text("ERROR: Unable to generate weather data. Try again later...")

    # Display all data as markdown text fields
    st.header(f"{city.upper()} WEATHER", divider="orange")
    st.subheader(":world_map: Location Details")
    st.markdown(f"Latitude: **{data.get('latitude')}**")
    st.markdown(f"Longitude: **{data.get('longitude')}**")
    st.markdown(
        f"Elevation: **{round(data.get('elevation') * METERS_TO_FEET_CONVERSION, 2)} feet**"
    )
    st.text("")
    st.subheader(":partly_sunny: Current Weather")
    st.markdown(f"Current Temperature: **{round(data.get('currentTemperature'))}°F**")
    st.markdown(f"Current Humidity: **{round(data.get('currentHumidity'))}%**")
    st.markdown(
        f"Current Precipitation: **{round(data.get('currentPrecipitation'))} inches**"
    )
    st.text("")
    st.subheader(f":clock3: Hourly Weather")
    st.text("Temperatures, Humidities, Precipitations, Precipitation Probabilities")
    for interval in data.get("hourlyTimeIntervals"):
        curr_index = (data.get("hourlyTimeIntervals")).index(interval)
        datetime_str = pd.to_datetime(interval, unit="s").strftime("%A %b %d, %I%p")
        if datetime_str[-4] == "0":
            datetime_str = datetime_str[:-4] + datetime_str[-3:]

        st.markdown(
            f"{datetime_str}  —  **{round(data.get('hourlyTemperatures')[curr_index])}°F**,   **{round(data.get('hourlyHumidities')[curr_index])}% humidity**,   **{round(data.get('hourlyPrecipitations')[curr_index], 3)} inches of precipitation** with **{round(data.get('hourlyPrecipitationProbabilities')[curr_index])}%**"
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
