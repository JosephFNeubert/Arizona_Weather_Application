# IMPORTS
import streamlit as st
import json
import subprocess
import pandas as pd
from PIL import Image


# Subprocess to run backend file to update JSON files
def fetch_data():
    subprocess.run(["python", "ArizonaWeatherFetch.py"], check=True)


# Frontend
banner = Image.open("Assets/Banner.png")
st.image(banner, use_container_width=True)
st.text("Beginning of application website")
