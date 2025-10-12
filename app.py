import streamlit as st
import json
import subprocess
import pandas as pd


def fetch_data():
    subprocess.run(["python", "ArizonaWeatherFetch.py"], check=True)
