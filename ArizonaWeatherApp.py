# IMPORTS
# Import OS and Dotenv to use .env
import os
from dotenv import load_dotenv, dotenv_values

# Import OpenMeteo along with other relevant API packages
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# Set up the OpenMeteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openMeteo = openmeteo_requests.Client(session=retry_session)
load_dotenv()

url = os.getenv("URL")
params = {
    # Locations in Order: Phoenix, Prescott
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
}

responses = openMeteo.weather_api(os.getenv("URL"), params=params)

print(f"Latitude: {responses[0].Latitude()}, Longitude: {responses[0].Longitude()}")
print(f"Latitude: {responses[1].Latitude()}, Longitude: {responses[1].Longitude()}")
