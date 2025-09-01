# import requests
import pandas as pd
import matplotlib.pyplot as plt
import ssl
import urllib.request
import json
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import numpy as np

''' The purpose of this script is only to return a list of predicted and past tidal data in a dataframe format.'''

############# JSON DATA FOR HIGH/LOW TIDE TIMES #############
def create_high_low_tide_times_url(starttime, endtime):
    ''' returns high/low tide times from sligo harbour tide bouy'''
    baseurl = r"https://erddap.marine.ie/erddap/tabledap/IMI_TidePrediction_HighLow"
    responsetype = r".json"
    querystart = "?"
    querytime = "time"
    querysep = "%2C"
    querytidetimecat = "tide_time_category"
    quertideheightlat = "Water_Level_ODM"
    querystation = "stationID"
    # querywater = "Water_Level_LAT" the tide predicitions are not at this water level
    querywater = "Water_Level_OD_Malin"
    variablesep = "&"
    stationname = r"stationID=%22Sligo%22"
    # 2025 https://erddap.marine.ie/erddap/tabledap/IMI_TidePrediction_HighLow.json?stationID%2Ctime%2Clongitude%2Clatitude%2Ctide_time_category%2CWater_Level_ODM&stationID%3E=%22Sligo%22&time%3E=2025-08-30T12%3A03%3A57Z&time%3C=2025-09-07T12%3A03%3A57Z
    url =  (baseurl + responsetype + querystart +
           querystation + querysep +
            querytime + querysep +
            querytidetimecat + querysep +
            quertideheightlat +
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
    try:
        with urllib.request.urlopen(url) as response:
            try:
                return json.load(response)
            except json.JSONDecodeError:
                print("Error: Failed to decode JSON response.")
                return None
    except urllib.error.HTTPError as http_err:
        print(f"HTTP Error: {http_err.code} - {http_err.reason}")
        return None
    except Exception as e:
        print(f"Error: Failed to fetch data from URL. {e}")
        return None
    
def convert_timestamp_to_numpy(timestamps_array):
    # Ensure input is a pandas Series of datetime64[ns]
    timestamps_array = pd.to_datetime(timestamps_array)
    return np.array(timestamps_array.astype('int64') // 10**9)

# Function to process data into DataFrame
def process_predicted_data(data):
    # Extract the table information
    df = pd.DataFrame(data['table']['rows'], columns=data['table']['columnNames'])
    # columnNames": ["time", "stationID", "sea_surface_height"],
    # Ensure correct data types
    df['time'] = pd.to_datetime(df['time'])  # Convert time to Ireland timezone
    df['tide_level'] = pd.to_numeric(df['sea_surface_height'])  # Convert water level to numeric
    return df

def process_high_low_tide_data(data):
    df = pd.DataFrame(data['table']['rows'], columns=data['table']['columnNames'])
    print(df.columns)
    sligo_to_streedagh_offset = 18
    df['time'] = pd.to_datetime(df['time']) - pd.Timedelta(minutes=sligo_to_streedagh_offset)
    df['tide_time_category'] = df['tide_time_category'].str.replace('High', 'High Tide')
    df['tide_time_category'] = df['tide_time_category'].str.replace('Low', 'Low Tide')
    return df

def fetch_and_format_tide_data():
    ''' 2025 update - historical and High/Low Tide Data dropped '''
    ########## Predicted Tide Data ##########
    time_range = 7
    formatted_start_time, formatted_end_time = format_time_range(time_range)
    url = create_predicted_tide_url(formatted_start_time, formatted_end_time)
    ssl._create_default_https_context = ssl._create_unverified_context
    data_predicted = fetch_data(url)
    df_predicted = process_predicted_data(data_predicted)

    ################## High/Low Tide Times ##################
    url = create_high_low_tide_times_url(formatted_start_time, formatted_end_time)
    ssl._create_default_https_context = ssl._create_unverified_context
    data_high_low = fetch_data(url)
    df_high_low = process_high_low_tide_data(data_high_low)
    return df_predicted, df_high_low

# create a test section that prints the URLS generated for each of the data calls
if __name__ == "__main__":
    time_range_pred = 7
    formatted_start_time_pred, formatted_end_time_pred = format_time_range(time_range_pred)

    url_pred = create_predicted_tide_url(formatted_start_time_pred, formatted_end_time_pred)
    url_high_low = create_high_low_tide_times_url(formatted_start_time_pred, formatted_end_time_pred)

    print("\nPredicted Tide Data URL:")
    print(url_pred)
    print("\nHigh/Low Tide Times URL:")
    print(url_high_low)