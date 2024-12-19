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

##########
#   run this to get the venv up
# source /Users/philipkevinbates/Documents/Coding/Tides/bin/activate 
# Need to have the venv in the same folder as the project folder I guess
###############################


# Function to create URL for tide data
def create_historical_tide_url(starttime, endtime):
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
    return (baseurl + responsetype + querystart +
            querytime + querysep + querywater + querysep + querystation +
            variablesep + starttime + variablesep + endtime + variablesep + stationname)

def create_predicted_tide_url(starttime, endtime):
    ############# JSON DATA FOR PREDICTED TIDE LEVELS #############
    # Define the URL for the data
    # https://erddap.marine.ie/erddap/tabledap/imiTidePredictionEpa.json?time%2CstationID%2Csea_surface_height&time%3E=2024-12-13T23%3A50%3A43Z&time%3C=2024-12-16T23%3A50%3A43Z&longitude%3E=-8.693&latitude%3E=54.4&stationID=%22IEWEBWC430_0000_0100_MODELLED%22
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

# Function to plot tide data
def plot_tide_data(df, label, color):
    plt.plot(df['time'], df['tide_level'], label=label, color=color)

# Function to create and save tide plot image
def create_tide_plot_image(df, filename):
    img = Image.new('RGB', (800, 480), 'white')
    draw = ImageDraw.Draw(img)
    timestamps = np.array(df['time'].astype(np.int64) // 10**9)
    water_levels = df['tide_level'].values
    water_levels_smooth = df['tide_level'].rolling(window=15, center=True).mean().values
    ## use predicted data
    # plot in the area Y 0 to 80 all the predicted data
    # plot in the area Y 80 to 320 only the predicted data for the current 24 hrs
    # plot on the 80 to 320 area the dot showing the current time
    # Show text for next high tide time
    # Show text for next low tide time
    
    # full range of predicted data
    def map_data_to_plot_area(testpoint, timestamps, water_levels, pxyarea, imgdim):
        imgx = imgdim[0]
        imgy = imgdim[1]
        pxmin = pxyarea[0]
        pxmax = pxyarea[1]
        pymin = pxyarea[2]
        pymax = pxyarea[3]
        x_min, x_max = timestamps.min(), timestamps.max()
        y_min, y_max = water_levels.min(), water_levels.max()
        x_normalized = (timestamps - x_min) / (x_max - x_min) * (pxmax - pxmin) + pxmin
        # Y pixels are inverted, 0,0 is top left
        y_normalized = pymax - (water_levels - y_min) / (y_max - y_min) * (pymax - pymin)
        ptx = (testpoint[0] - x_min) / (x_max - x_min) * (pxmax - pxmin) + pxmin
        pty = pymax - (testpoint[1] - y_min) / (y_max - y_min) * (pymax - pymin)
        return x_normalized, y_normalized, ptx, pty
    

    current_time = datetime.now(timezone.utc).timestamp()
    closest_index = np.abs(timestamps - current_time).argmin()
    print(f"current_time: {current_time}")
    print(f"closest_index: {closest_index}")

    ptxy = [timestamps[closest_index], water_levels[closest_index]]

    ####### filtered 24hr data plot #######
    time_lower_limit = current_time - 12 * 60 * 60
    time_upper_limit = current_time + 12 * 60 * 60
    filtered_timestamps = timestamps[(timestamps >= time_lower_limit) & (timestamps <= time_upper_limit)]
    filtered_water_levels = water_levels[(timestamps >= time_lower_limit) & (timestamps <= time_upper_limit)]
    x_normalized, y_normalized, ptx, pty = map_data_to_plot_area(ptxy,filtered_timestamps, filtered_water_levels, (0, 800, 100, 300), (800, 480))
    points = list(zip(x_normalized, y_normalized))
    draw.polygon([(0, 480)] + points + [(800, 480)], fill='lightgrey')
    # Draw a solid line for the water level at all timestamps up to the present time
    past_times = timestamps[(timestamps >= time_lower_limit)& (timestamps <= current_time)]
    past_water_levels = water_levels[(timestamps >= time_lower_limit)& (timestamps <= current_time)]
    x_normalized, y_normalized,_,_  = map_data_to_plot_area(ptxy, past_times, past_water_levels, (0, 800, 100, 300), (800, 480))
    points = list(zip(x_normalized, y_normalized))
    # draw.line(points, fill='black', width=2)
    # Mark the current time with a sphere
    ptradius = 5
    draw.ellipse((ptx - ptradius, pty- ptradius, ptx + ptradius, pty + ptradius), fill='black')
    ptradius = 2
    draw.ellipse((ptx - ptradius, pty- ptradius, ptx + ptradius, pty + ptradius), fill='white')
    
    # mark high tide
    # get the max and min values and timestamps for the filtered data
    max_index = np.argmax(filtered_water_levels)
    min_index = np.argmin(filtered_water_levels)
    HighTidexy = [filtered_timestamps[max_index], filtered_water_levels[max_index]]
    LowTidexy = [filtered_timestamps[min_index], filtered_water_levels[min_index]]
    # # convert the max and min values to the pixel positions using map_data_to_plot_area
    x_normalized, y_normalized,HighTidex, HighTidey = map_data_to_plot_area(HighTidexy,filtered_timestamps, filtered_water_levels, (0, 800, 100, 300), (800, 480))
    x_normalized, y_normalized,LowTidex, LowTidey = map_data_to_plot_area(LowTidexy,filtered_timestamps, filtered_water_levels, (0, 800, 100, 300), (800, 480))
    # # at the high tide, draw a vertical line from high tide down by 1/2 the area being used
    draw.line((HighTidex, HighTidey, HighTidex, HighTidey+100), fill='black')
    draw.line((LowTidex, LowTidey, LowTidex, LowTidey-100), fill='black')
    ptradius = 2
    draw.ellipse((HighTidex - ptradius, HighTidey- ptradius, HighTidex + ptradius, HighTidey + ptradius), fill='black')
    # add text for high tide
    font = ImageFont.load_default()
    label_time = datetime.fromtimestamp(filtered_timestamps[max_index], timezone.utc).strftime('%H:%M')
    draw.text((HighTidex-10, HighTidey+110), label_time, fill='black', font=font, align='center')
    ptradius = 2
    draw.ellipse((LowTidex - ptradius, LowTidey- ptradius, LowTidex + ptradius, LowTidey + ptradius), fill='black')
    label_time = datetime.fromtimestamp(filtered_timestamps[min_index], timezone.utc).strftime('%H:%M')
    draw.text((LowTidex-10, LowTidey-120), label_time, fill='black', font=font, align='center')
    ####### full historical + predicted data plot #######
    x_normalized, y_normalized, ptx, pty = map_data_to_plot_area(ptxy,timestamps, water_levels, (0, 800, 330, 470), (800, 480))
    points = list(zip(x_normalized, y_normalized))
    draw.polygon([(0, 480)] + points + [(800, 480)], fill='black')
    # Mark the current time with a sphere
    ptradius = 4
    draw.ellipse((ptx - ptradius, pty- ptradius, ptx + ptradius, pty + ptradius), fill='white')
    ptradius = 2
    draw.ellipse((ptx - ptradius, pty- ptradius, ptx + ptradius, pty + ptradius), fill='black')


    # Mark boundaries of tide data
    draw.line((0, 330, 800, 330), fill='black')
    draw.line((0, 400, 800, 400), fill='black')
    draw.line((0, 470, 800, 470), fill='white')
   


    # font = ImageFont.load_default()
    # time_labels = [x_min, x_min + 0.25 * (x_max - x_min), x_min + 0.75 * (x_max - x_min), x_max]
    # for i, label in enumerate(time_labels):
    #     label_time = datetime.utcfromtimestamp(label).strftime('%Y-%m-%d %H:%M:%S')
    #     draw.text((i * 200, 400), label_time, fill='black', font=font)
    img.save(filename)
    img.show()

# Main function

########## Historical Tide Data ##########
time_range = 10
formatted_start_time, formatted_end_time = format_time_range(time_range)
url = create_historical_tide_url(formatted_start_time, formatted_end_time)
ssl._create_default_https_context = ssl._create_unverified_context
#only fetch data if the dataframes are empty
# data_historical = fetch_data(url)

df_historical = process_historical_data(data_historical)

########## Predicted Tide Data ##########
time_range = 7
formatted_start_time, formatted_end_time = format_time_range(time_range)
url = create_predicted_tide_url(formatted_start_time, formatted_end_time)
ssl._create_default_https_context = ssl._create_unverified_context

# data_predicted = fetch_data(url)
df_predicted = process_predicted_data(data_predicted)


# merge the dataframes on time, starting from the end of the historical data only
df_predicted_cut = df_predicted[df_predicted['time'] > df_historical['time'].max()]
df_historical_cut = df_historical[df_historical['time'] < df_predicted_cut['time'].min()]
df_merged = pd.concat([df_historical_cut, df_predicted_cut])
# Plot the tide data
plt.figure(figsize=(12, 6))
plot_tide_data(df_historical, 'Historical Tide Level (LAT)', 'blue')
plot_tide_data(df_predicted, 'Predicted Tide Level (LAT)', 'red')
plot_tide_data(df_merged, 'Merged Tide Level (LAT)', 'green')
plt.xlabel('Time')
plt.ylabel('Tide Level (m relative to LAT)')
plt.title('Tide Level Over Time (Sligo Station)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
create_tide_plot_image(df_merged, 'tide_plot.png')


