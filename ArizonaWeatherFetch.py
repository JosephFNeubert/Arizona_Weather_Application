"""
File: ArizonaWeatherFetch.py
Author: Joseph Neubert
Description: Application backend that accesses interfaces with the Open-Meteo API in order to fetch weather data for multiple cities
within Arizona based on defined parameters. Each city's current weather data, location details, and list of hourly weather changes
are compiled into a dictionary, and that dictionary is dumped into their own respective JSON files in the Data directory for future
processing and display.

"""

# IMPORTS
# Import Open-Meteo for API requests along with other relevant packages
import openmeteo_requests
import pandas as pd
import numpy as np
import requests_cache
from retry_requests import retry

import json
import streamlit as st

# CONSTANT
NUMBER_OF_DATETIMES = 168

# Set up the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openMeteo = openmeteo_requests.Client(session=retry_session)

# Establish Open-Meteo URL and parameters for API calls
url = st.secrets["url"]
params = {
    ### Locations in Order: Phoenix, Prescott ###
    # TODO: Add more cities (their latitudes and longitudes)
    "latitude": [33.448206, 34.541246],
    "longitude": [-112.073789, -112.469394],
    # Hourly and current conditions
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "precipitation_probability",
    ],
    "current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
    "temperature_unit": "fahrenheit",
}

# Call Open-Meteo API and store in responses list
responses = openMeteo.weather_api(url, params=params)

# File path to the data for each city
# TODO: Include added cities into this tuple
cities_tuple = ("Data/Phoenix.json", "Data/Prescott.json")

# Each API response corresponds to one city's data
iteration = 0
for response in responses:
    # Each city location details
    latitude = response.Latitude()
    longitude = response.Longitude()
    elevation = response.Elevation()

    # Each city hourly temperature, humidity, precipitation, and precipitation probability conditions
    hourly = response.Hourly()
    hourlyTemperatures = hourly.Variables(0).ValuesAsNumpy()
    hourlyHumidities = hourly.Variables(1).ValuesAsNumpy()
    hourlyPrecipitations = hourly.Variables(2).ValuesAsNumpy()
    hourlyPrecipitationProbs = hourly.Variables(3).ValuesAsNumpy()
    hourlyTimeIntervals = np.empty(NUMBER_OF_DATETIMES)
    count = 0
    for x in range(
        hourly.Time(),
        hourly.TimeEnd(),
        hourly.Interval(),
    ):
        hourlyTimeIntervals[count] = x
        count += 1

    # Each city current temperature, humidity, and precipitation conditions
    current = response.Current()
    currentTemperature = current.Variables(0).Value()
    currentRelativeHumidity = current.Variables(1).Value()
    currentPrecipitation = current.Variables(2).Value()

    # Create a dictionary for each city to be dumped into a JSON file
    city = {}
    city["latitude"] = latitude
    city["longitude"] = longitude
    city["elevation"] = elevation
    city["currentTemperature"] = currentTemperature
    city["currentHumidity"] = currentRelativeHumidity
    city["currentPrecipitation"] = currentPrecipitation
    city["hourlyTimeIntervals"] = hourlyTimeIntervals.tolist()
    city["hourlyTemperatures"] = hourlyTemperatures.tolist()
    city["hourlyHumidities"] = hourlyHumidities.tolist()
    city["hourlyPrecipitations"] = hourlyPrecipitations.tolist()
    city["hourlyPrecipitationProbabilities"] = hourlyPrecipitationProbs.tolist()

    with open(cities_tuple[iteration], "w") as f:
        json.dump(city, f)
    iteration += 1
