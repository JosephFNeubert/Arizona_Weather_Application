# IMPORTS
import json
import streamlit as st

# Import OpenMeteo along with other relevant API packages
import openmeteo_requests
import pandas as pd
import numpy as np
import requests_cache
from retry_requests import retry

# Constants
NUMBER_OF_DATETIMES = 168

# Set up the OpenMeteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openMeteo = openmeteo_requests.Client(session=retry_session)

# Establish Open-Meteo URL and parameters for API calls
url = st.secrets["url"]
params = {
    ### Locations in Order: Phoenix, Prescott ###
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

# Cities tuple
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

    # Create a dictionary for each city to be dumped into a json file
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
