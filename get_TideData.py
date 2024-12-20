import requests
import pandas as pd
import matplotlib.pyplot as plt
import ssl
import urllib.request
import json
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import numpy as np
# from .MetEireann import create_weather_image

''' The purpose of this script is only to return a list of predicted and past tidal data in a dataframe format.'''

############# JSON DATA FOR **PAST** TIDE LEVELS #############
# Function to create URL for tide data

def create_historical_tide_url(starttime, endtime):
    ''' returns past data from sligo harbour tide bouy'''
    baseurl = r"https://erddap.marine.ie/erddap/tabledap/IrishNationalTideGaugeNetwork"
    responsetype = r".json"
    querystart = "?"
    querytime = "time"
    querysep = "%2C"
    querystation = "station_id"
    # querywater = "Water_Level_LAT" the tide predicitions are not at this water level
    querywater = "Water_Level_OD_Malin"
    variablesep = "&"
    stationname = r"station_id=%22Sligo%22"
    url =  (baseurl + responsetype + querystart +
            querytime + querysep + querywater + querysep + querystation +
            variablesep + starttime + variablesep + endtime + variablesep + stationname)
    return url

############# JSON DATA FOR PREDICTED TIDE LEVELS #############
def create_predicted_tide_url(starttime, endtime):
    ''' returns future data at streedagh beach'''
    # Define the URL for the data
    baseurl = r"https://erddap.marine.ie/erddap/tabledap/imiTidePredictionEpa"
    responsetype = r".json"
    querystart = "?"
    querytime = "time"
    querysep = "%2C"
    querystation = "stationID"
    #querysep after querystation
    querywater = "sea_surface_height"
    variablesep = "&"
    # starttime = r"time%3E=2024-12-13T23%3A50%3A43Z"
    #variablesep after starttime
    # endtime = r"time%3C=2024-12-16T23%3A50%3A43Z"
    stationname = r"stationID=%22IEWEBWC430_0000_0100_MODELLED%22"
    # Define the new URL with the updated time
    url = (baseurl + responsetype + querystart +
        querytime + querysep + querywater + querysep + querystation +
        variablesep + starttime + variablesep + endtime+ variablesep + stationname)
    return url

def format_time_range(range):
    current_time = datetime.now(timezone.utc)
    current_time_minus_range = current_time - timedelta(days=range)
    current_time_plus_range = current_time + timedelta(days=range)
    formatted_start_time = r"time%3E=" + current_time_minus_range.strftime("%Y-%m-%dT%H:%M:%SZ").replace(":", "%3A")
    formatted_end_time = r"time%3C=" + current_time_plus_range.strftime("%Y-%m-%dT%H:%M:%SZ").replace(":", "%3A")
    return formatted_start_time, formatted_end_time

# Function to fetch data from URL
def fetch_data(url):
    with urllib.request.urlopen(url) as response:
        return json.load(response)

# Function to process data into DataFrame
def process_historical_data(data):
    df = pd.DataFrame(data['table']['rows'], columns=data['table']['columnNames'])
    df['time'] = pd.to_datetime(df['time'])
    # df['tide_level'] = pd.to_numeric(df['Water_Level_LAT'])
    df['tide_level'] = pd.to_numeric(df['Water_Level_OD_Malin'])
    return df

# Function to process data into DataFrame
def process_predicted_data(data):
    # Extract the table information
    df = pd.DataFrame(data['table']['rows'], columns=data['table']['columnNames'])
    # columnNames": ["time", "stationID", "sea_surface_height"],
    # Ensure correct data types
    df['time'] = pd.to_datetime(df['time'])  # Convert time to datetime format
    df['tide_level'] = pd.to_numeric(df['sea_surface_height'])  # Convert water level to numeric
    return df

def fetch_and_format_tide_data():
    ########## Historical Tide Data ##########
    time_range = 10
    formatted_start_time, formatted_end_time = format_time_range(time_range)
    url = create_historical_tide_url(formatted_start_time, formatted_end_time)
    ssl._create_default_https_context = ssl._create_unverified_context
    #only fetch data if the dataframes are empty
    data_historical = fetch_data(url)
    df_historical = process_historical_data(data_historical)

    ########## Predicted Tide Data ##########
    time_range = 7
    formatted_start_time, formatted_end_time = format_time_range(time_range)
    url = create_predicted_tide_url(formatted_start_time, formatted_end_time)
    ssl._create_default_https_context = ssl._create_unverified_context
    data_predicted = fetch_data(url)
    df_predicted = process_predicted_data(data_predicted)
    return df_historical, df_predicted