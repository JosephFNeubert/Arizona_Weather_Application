"""
File: ArizonaWeatherFetch.py
Author: Joseph Neubert
Description: Application backend that accesses interfaces with the Open-Meteo API in order to fetch weather data for multiple cities
within Arizona based on defined parameters. Each city's current weather data, location details, and list of hourly weather changes
are compiled into a dictionary, and that dictionary is appended to a list that is accessed for processing and display of data.

"""

# IMPORTS
# Import Open-Meteo for API requests along with other relevant packages
import openmeteo_requests
import pandas as pd
import numpy as np
import requests_cache
from retry_requests import retry
import streamlit as st

# CONSTANT
NUMBER_OF_DATETIMES = 168


def weather_fetch(location: int) -> list[dict]:
    """
    Principal backend function that interfaces with Open-Meteo API to produce and return cities' weather data.
    """
    # Set up the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openMeteo = openmeteo_requests.Client(session=retry_session)

    # Establish Open-Meteo URL and parameters for API calls
    url = st.secrets["url"]

    ### Locations in Order: Phoenix (Metro), Prescott, Flagstaff, Tucson, Sedona, Payson, Page, Yuma, Lake Havasu City, Casa Grande ###
    #
    # Add more cities here (their latitudes and longitudes)
    #
    latitudes_list = [
        33.448206,
        34.541246,
        35.198243,
        32.254004,
        34.863726,
        34.230812,
        36.914891,
        32.693005,
        34.477682,
        32.879606,
    ]
    longitudes_list = [
        -112.073789,
        -112.469394,
        -111.652078,
        -110.971988,
        -111.796931,
        -111.325100,
        -111.455649,
        -114.627744,
        -114.319913,
        -111.740032,
    ]

    # Set parameters for hourly and current conditions and the particular location of the a selected city
    latitude = latitudes_list[location]
    longitude = longitudes_list[location]
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "precipitation_probability",
        ],
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }

    # Call Open-Meteo API and store in responses list
    response = openMeteo.weather_api(url, params=params)

    # Each API response corresponds to one city's data
    # Each city location details
    latitude = response[0].Latitude()
    longitude = response[0].Longitude()
    elevation = response[0].Elevation()

    # Each city hourly temperature, humidity, precipitation, and precipitation probability conditions
    hourly = response[0].Hourly()
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
    current = response[0].Current()
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

    return city
