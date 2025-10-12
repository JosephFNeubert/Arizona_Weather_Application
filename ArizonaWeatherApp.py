# IMPORTS
# Import OS and Dotenv to use .env
import os
from dotenv import load_dotenv, dotenv_values
import json
import matplotlib.pyplot as plt

# Import OpenMeteo along with other relevant API packages
import openmeteo_requests
import pandas as pd
import numpy as np
import requests_cache
from retry_requests import retry

# Set up the OpenMeteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openMeteo = openmeteo_requests.Client(session=retry_session)
load_dotenv()  # Parse .env for API URL

# Establish Open-Meteo URL and parameters for API calls
url = os.getenv("URL")
params = {
    # *Locations in Order: Phoenix, Prescott*
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
responses = openMeteo.weather_api(os.getenv("URL"), params=params)

# Lists for all weather values retrieved by API
latitudes = []
longitudes = []
elevations = []
hourlyTemperatures = []
hourlyHumidities = []
hourlyPrecipitations = []
hourlyPrecipitationProbs = []
hourlyTimeIntervals = []
currentTemperature = []
currentRelativeHumidity = []
currentPrecipitation = []

# To populate all lists
for response in responses:
    # Each city location details
    latitudes.append(response.Latitude())
    longitudes.append(response.Longitude())
    elevations.append(response.Elevation())

    # Each city hourly temperature, humidity, precipitation, and precipitation probability conditions
    hourly = response.Hourly()
    hourlyTemperatures.append(hourly.Variables(0).ValuesAsNumpy())
    hourlyHumidities.append(hourly.Variables(1).ValuesAsNumpy())
    hourlyPrecipitations.append(hourly.Variables(2).ValuesAsNumpy())
    hourlyPrecipitationProbs.append(hourly.Variables(3).ValuesAsNumpy())
    hourlyData = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.to_datetime(hourly.Interval(), unit="s"),
            inclusive="left",
        )
    }
    hourlyData["temperature_2m"] = hourlyTemperatures
    hourlyData["relative_humidity_2m"] = hourlyHumidities
    hourlyData["precipitation"] = hourlyPrecipitations
    hourlyData["precipitation_probability"] = hourlyPrecipitationProbs
    hourlyDataframe = pd.DataFrame(data=hourlyData)

    # Each city current temperature, humidity, and precipitation conditions
    current = response.Current()
    currentTemperature.append(current.Variables(0).Value())
    currentRelativeHumidity.append(current.Variables(1).Value())
    currentPrecipitation.append(current.Variables(2).Value())


# TESTING PURPOSES ONLY
# print(f"Latitude: {responses[0].Latitude()}, Longitude: {responses[0].Longitude()}")
# print(f"Latitude: {responses[1].Latitude()}, Longitude: {responses[1].Longitude()}")
# city1Times = hourlyTimeIntervals[0]
# city2Times = hourlyTimeIntervals[1]
# print(city1Times[0])
# print(city2Times[0])
# print(pd.to_datetime(city1Times[0], unit="s"))
# print(pd.to_datetime(city2Times[0], unit="s"))
# plt.plot(hourlyDataframe["te"])
print(hourlyDataframe)
