import requests
import pandas as pd
import matplotlib.pyplot as plt
# import ssl
# import urllib.request
# import json
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import numpy as np
# from .MetEireann import create_weather_image
import get_MetEireann
import get_TideData



##########
#   run this to get the venv up
# source /Users/philipkevinbates/Documents/Coding/Tides/bin/activate 
# Need to have the venv in the same folder as the project folder I guess
###############################

class DataToPlotAreaMapper:
    '''Class to map data points to a specific area on the plot
    inputs:
    timestamps: numpy array of timestamps
    water_levels: numpy array of water levels
    pxyarea: tuple of (xmin, xmax, ymin, ymax) for the plot area
    imgdim: tuple of (x, y) for the image dimensions
    '''

    def __init__(self, timestamps, water_levels, pxyarea, imgdim):
        timestamps = np.array(timestamps)
        water_levels = np.array(water_levels)
        self.imgx = imgdim[0]
        self.imgy = imgdim[1]
        self.pxmin = pxyarea[0]
        self.pxmax = pxyarea[1]
        self.pymin = pxyarea[2]
        self.pymax = pxyarea[3]
        self.x_min = timestamps.min()
        self.x_max = timestamps.max()
        self.y_min = water_levels.min()
        self.y_max = water_levels.max()

    def map_point(self, point):
        x, y = point
        ptx = (x - self.x_min) / (self.x_max - self.x_min) * (self.pxmax - self.pxmin) + self.pxmin
        pty = self.pymax - (y - self.y_min) / (self.y_max - self.y_min) * (self.pymax - self.pymin)
        return ptx, pty

    def map_vectors(self, x_vector, y_vector):
        x_normalized = (x_vector - self.x_min) / (self.x_max - self.x_min) * (self.pxmax - self.pxmin) + self.pxmin
        y_normalized = self.pymax - (y_vector - self.y_min) / (self.y_max - self.y_min) * (self.pymax - self.pymin)
        return x_normalized, y_normalized


# # Adjust times from UTC to current local time
# def utc_to_local(utc_dt):
#         local_tz = pytz.timezone("Europe/London")
#         return utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)


# Function to plot tide data
def plot_tide_data(df, label, color):
    plt.plot(df['time'], df['tide_level'], label=label, color=color)

def draw_point(draw, ptx, pty, radius):
    ptradius = max(1, radius +1)
    draw.ellipse((ptx - ptradius, pty - ptradius, ptx + ptradius, pty + ptradius), fill='white')
    ptradius = radius
    draw.ellipse((ptx - ptradius, pty - ptradius, ptx + ptradius, pty + ptradius), fill='black')
    ptradius = max(1, radius - 3)
    draw.ellipse((ptx - ptradius, pty - ptradius, ptx + ptradius, pty + ptradius), fill='white')

def draw_diamond(draw, center_x, center_y, size):
    half_size = size / 2
    h_squash = 0.6
    points = [
        (center_x, center_y - half_size),  # Top
        (center_x + half_size*h_squash, center_y),  # Right
        (center_x, center_y + half_size),  # Bottom
        (center_x - half_size*h_squash, center_y)   # Left
    ]
    b = 3
    points_mid = [
        (center_x, center_y - half_size-b),  # Top
        (center_x + half_size*h_squash+b, center_y),  # Right
        (center_x, center_y + half_size+b),  # Bottom
        (center_x - half_size*h_squash-b, center_y)   # Left
    ]
    b = 5
    points_out = [
        (center_x, center_y - half_size-b),  # Top
        (center_x + half_size*h_squash+b, center_y),  # Right
        (center_x, center_y + half_size+b),  # Bottom
        (center_x - half_size*h_squash-b, center_y)   # Left
    ]
    draw.polygon(points_out, fill='black', outline='grey', width=2)
    draw.polygon(points_mid, fill='black', outline='black', width=1)
    draw.polygon(points, fill='white', outline='grey', width=3)

def mark_tide_time(draw, mapper, df_highlow_tides):
    # Draw a point at the time
    # Draw a line down from the high tide time, colored black
    # place text at the bottom of the line
    font = ImageFont.truetype("Work-Sans-1.50/fonts/webfonts/ttf/WorkSans-Medium.ttf", size=44)

    for index, row in df_highlow_tides.iterrows():
        label_time = datetime.fromtimestamp(row['closest_time'], timezone.utc).strftime('%H:%M')
        tide_xy = [row['closest_time'], row['closest_water_level']]
        tide_x, tide_y = mapper.map_point(tide_xy)
        tide_type = row['tide_time_category']
        draw_point(draw, tide_x, tide_y, 6)
        # draw the line
        if tide_type == "HIGH":
            draw.line((tide_x, tide_y, tide_x, 212), fill='white')
        elif tide_type == "LOW":
            draw.line((tide_x, tide_y, tide_x, 88), fill='black')
        # add the label
        t_xoff = 4
        if tide_type == "HIGH":
            draw.text((tide_x+t_xoff, 220), label_time, fill='white', font=font, anchor='mt')
        elif tide_type == "LOW":
            draw.text((tide_x-t_xoff, 80), label_time, fill='black', font=font, anchor='ms')
        print(f"Tide time: {label_time} located at {tide_x, tide_y}")

# Function to create and save tide plot image
def create_tide_plot_image(df, df_high_low, filename):
    
    img_dimensions = (800, 480)
    img = Image.new('RGB', img_dimensions, 'white')
    draw = ImageDraw.Draw(img)
    
    #establish time windows
    timestamps = np.array(df['time'].astype(np.int64) // 10**9)
    current_time = datetime.now(timezone.utc).timestamp()
    closest_index = np.abs(timestamps - current_time).argmin()
    print(f"current_time: {current_time}")
    print(f"closest_index: {closest_index}")



    # create a 24hr window around the current time
    time_lower_limit_24hr = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    time_upper_limit_24hr = time_lower_limit_24hr + 24 * 60 * 60
    time_lower_limit_full = timestamps.min()
    time_upper_limit_full = timestamps.max()
    tide_upper_limit =  2
    tide_lower_limit = -2
    time_span_24hr = [time_lower_limit_24hr, time_upper_limit_24hr]
    time_span_full = [time_lower_limit_full, time_upper_limit_full]
    tide_span = [tide_lower_limit, tide_upper_limit]


    # get the tide data
    water_levels = df['tide_level'].values

    # plot in the area Y 0 to 80 all the predicted data
    # plot in the area Y 80 to 320 only the data for the current 24 hrs
    # px_for_weather = (0, 800, 0, 80)
    px_for_24hr = (0, 800, 30, 300)
    px_for_full = (0, 800, 310, 470)
    mapper_24hr = DataToPlotAreaMapper(time_span_24hr, tide_span, px_for_24hr, img_dimensions)
    mapper_full = DataToPlotAreaMapper(time_span_full, tide_span, px_for_full, img_dimensions)


    # get now point
    pt_now = [timestamps[closest_index], water_levels[closest_index]]


    #################################################################################
    ####### filtered 24hr data plot #######
    #################################################################################
    timestamps24hr = timestamps[(timestamps >= time_span_24hr[0]) & (timestamps <= time_span_24hr[1])]
    tide_24hr = water_levels[(timestamps >= time_span_24hr[0]) & (timestamps <= time_span_24hr[1])]
    past_times = timestamps[(timestamps >= time_span_24hr[0]) & (timestamps <= current_time)]
    past_water_levels = water_levels[(timestamps >= time_span_24hr[0]) & (timestamps <= current_time)]
    future_times = timestamps[(timestamps > current_time) & (timestamps <= time_span_24hr[1])]
    future_water_levels = water_levels[(timestamps > current_time) & (timestamps <= time_span_24hr[1])]

    #draw the shaded data plot
    x_px_24r, y_px_24hr = mapper_24hr.map_vectors(timestamps24hr, tide_24hr)
    points = list(zip(x_px_24r, y_px_24hr ))
    draw.polygon([(0, 480)] + points + [(800, 480)], fill='black')
    
    # Draw a solid line for the water level at all timestamps up to the present time
    x_normalized, y_normalized = mapper_24hr.map_vectors(past_times, past_water_levels)
    points = list(zip(x_normalized, y_normalized))
    draw.line(points, fill='grey', width=2)


    ######################################################################################
    ####### current,  high and low tide times marked #######
    # Mark the current time with a sphere
    ptx, pty = mapper_24hr.map_point(pt_now)
    # draw_point(draw, ptx, pty, radius=6)
    draw_diamond(draw, ptx, pty, size=30)

    # Find the next four high and low tide entries after the current time
    current_time_dt = pd.to_datetime(time_lower_limit_24hr, unit='s', utc=True)
    next_high_low_tides = df_high_low[df_high_low['time'] > current_time_dt].head(4)
    print(next_high_low_tides)


    for index, row in next_high_low_tides.iterrows():
        closest_index = np.abs(df['time'] - row['time']).argmin()
        closest_time = timestamps[closest_index]
        closest_water_level = water_levels[closest_index]
        # print(f"Closest time: {closest_time}, Closest water level: {closest_water_level}")
        next_high_low_tides.at[index, 'closest_time'] = closest_time
        next_high_low_tides.at[index, 'closest_water_level'] = closest_water_level


    # Add the update time in the top left corner
    font = ImageFont.truetype("Work-Sans-1.50/fonts/webfonts/ttf/WorkSans-Medium.ttf", size=12)
    update_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    draw.text((10, 10), f"updated: {update_time}", fill='black', font=font)

    mark_tide_time(draw, mapper_24hr, next_high_low_tides)
    # treat the high tide time


    

    

    # # Draw point and text for high tide within next 10 hours
    # draw_point(draw, HighTidex_10hr, HighTidey_10hr, 6)
    # label_time_10hr = datetime.fromtimestamp(future_10hr_times[max_10hr_index], timezone.utc).strftime('%H:%M')
    # draw.text((HighTidex_10hr, HighTidey_10hr + 5), label_time_10hr, fill='blue', font=font, anchor='ms')
    # print(f"High tide within next 10 hours time: {label_time_10hr} located at {HighTidex_10hr, HighTidey_10hr}")
    # max_index = np.argmax(future_water_levels)
    # min_index = np.argmin(future_water_levels)
    # HighTidexy = [future_times[max_index], future_water_levels[max_index]]
    # LowTidexy = [future_times[min_index], future_water_levels[min_index]]
    # print(f'High tide index: {max_index}, Low tide index: {min_index}')
    # print(f'High tide time: {datetime.fromtimestamp(future_times[max_index], timezone.utc)}')
    # HighTidex, HighTidey = mapper_24hr.map_point(HighTidexy)
    # LowTidex, LowTidey = mapper_24hr.map_point(LowTidexy)

    # #draw vertical lines for high and low tide
    # draw.line((HighTidex, HighTidey, HighTidex, HighTidey + 50), fill='white')
    # draw.line((LowTidex, LowTidey, LowTidex, LowTidey - 50), fill='black')
    
    # font = ImageFont.truetype("Work-Sans-1.50/fonts/webfonts/ttf/WorkSans-Medium.ttf", size=44)
    # # draw points and text for high tide
    # draw_point(draw, HighTidex, HighTidey, 6)
    # label_time = datetime.fromtimestamp(future_times[max_index], timezone.utc).strftime('%H:%M')
    # draw.text((HighTidex, LowTidey+5), label_time, fill='white', font=font, anchor='ms')
    # print(f"High tide time: {label_time} located at {HighTidex, HighTidey}")
    
    # # draw points and text for low tide
    # draw_point(draw, LowTidex, LowTidey, 6)
    # label_time = datetime.fromtimestamp(future_times[min_index], timezone.utc).strftime('%H:%M')
    # draw.text((LowTidex, HighTidey-5), label_time, fill='black', font=font, anchor='mt')
    # print(f'Low tide time: {datetime.fromtimestamp(future_times[min_index], timezone.utc)}')

    #################################################################################
    ####### full historical + predicted data plot #######
    #################################################################################
    timestamps_full = timestamps[(timestamps >= time_span_full[0]) & (timestamps <= time_span_full[1])]
    tide_full = water_levels[(timestamps >= time_span_full[0]) & (timestamps <= time_span_full[1])]
    x_normalized, y_normalized = mapper_full.map_vectors(timestamps, water_levels)
    points = list(zip(x_normalized, y_normalized))
    draw.polygon([(0, 480)] + points + [(800, 480)], fill='grey')

    x_px_24r, y_px_24hr = mapper_full.map_vectors(timestamps24hr, tide_24hr)
    points = list(zip(x_px_24r, y_px_24hr ))
    draw.polygon([(x_px_24r.min(), 480)] + points + [(x_px_24r.max(), 480)], fill='white')
    
    # Mark the current time with a sphere
    ptx, pty = mapper_full.map_point(pt_now)
    draw_point(draw, ptx, pty, 6)
    window24hr_low = mapper_full.map_point([time_lower_limit_24hr, pty])
    window24hr_high = mapper_full.map_point([time_upper_limit_24hr, pty])


    # Mark boundaries of tide data
    draw.line((0, px_for_full[2], 800, px_for_full[2]), fill='grey')
    draw.line((0, 400, 800, 400), fill='black')
    draw.line((0, px_for_full[3], 800, px_for_full[3]), fill='black')
   


    # font = ImageFont.load_default()
    # time_labels = [x_min, x_min + 0.25 * (x_max - x_min), x_min + 0.75 * (x_max - x_min), x_max]
    # for i, label in enumerate(time_labels):
    #     label_time = datetime.utcfromtimestamp(label).strftime('%Y-%m-%d %H:%M:%S')
    #     draw.text((i * 200, 400), label_time, fill='black', font=font)
    img.save(filename)
    img.show()
    return img, draw, font

def create_weather_image(weather_data, img, draw, font):
    #establish time windows
    current_time = datetime.now(timezone.utc).timestamp()
    # create an array of times using the date from current time and each hour like 00:00, 01:00, 02:00 etc etc
    # Get today's date at 00:00 in UTC
    today_midnight = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    # Create an array of times for each hour of the current day
    timestamps_24hr = np.array([today_midnight + i * 3600 for i in range(25)])
    px_for_weather = (0, 800, 0, 80)
    mapper_weather = DataToPlotAreaMapper([today_midnight, today_midnight + 24 * 3600],
                                          [0,1], px_for_weather, img.size)
    for hour in timestamps_24hr:
        # convert the hour to the correct format to match the weather data key
        hour_key = datetime.fromtimestamp(hour, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        # get the symbol for this hour from the weather data
        symbol = weather_data.get(hour_key, {}).get('symbol', 'xf075')
        # convert the symbol to unicode
        unicode = get_MetEireann.get_unicode_value(symbol)

        print(f'Hour: {hour}, Symbol: {symbol}, Unicode: {unicode}')
        hourxy = (hour, 0.5)
        hr_x, hr_y = mapper_weather.map_point(hourxy)
        # draw vertical lines between each hour of the weather data
        font = ImageFont.truetype(r"weather-icons-master\font\weathericons-regular-webfont.ttf", size=32)
        # draw points and text for high tide
        draw.text((hr_x, hr_y), unicode, fill='black', font=font, anchor='ms')
        # draw.text((200, 100), "test", fill='black', font=font, anchor='ms')


    
    # Draw the weather data

    # Save and display the image
    img.save('weather_plot.png')
    img.show()




# Main function
#################################################################################
####### Tide Data ##########
# Get tide data from the ERDP open data website of the marine institute
df_historical, df_predicted, df_high_low = get_TideData.fetch_and_format_tide_data()

# merge the dataframes on time, starting from the end of the historical data only
df_predicted_cut = df_predicted[df_predicted['time'] > df_historical['time'].max()]
df_historical_cut = df_historical[df_historical['time'] < df_predicted_cut['time'].min()]
df_merged = pd.concat([df_historical_cut, df_predicted_cut])
df_merged = df_predicted


# write to screen using ScreenWriter.py
# from ScreenWriter import write_to_screen
# every minute until the script is killed
# start a clock at the current time
script_start_time = datetime.now(timezone.utc).timestamp()

img, draw, font = create_tide_plot_image(df_merged, df_high_low, 'tide_plot.png')
# write_to_screen(img, 60)
elapsed_time = datetime.now(timezone.utc) - datetime.fromtimestamp(script_start_time, timezone.utc)
if elapsed_time > timedelta(hours=12):
    df_historical, df_predicted, df_high_low = get_TideData.fetch_and_format_tide_data()
    df_predicted_cut = df_predicted[df_predicted['time'] > df_historical['time'].max()]
    df_historical_cut = df_historical[df_historical['time'] < df_predicted_cut['time'].min()]
    df_merged = pd.concat([df_historical_cut, df_predicted_cut])
    df_merged = df_predicted



#################################################################################
####### Weather Data ##########
# time_now = datetime.now(timezone.utc)
# Get weather data from the Met Eireann website
# weather_data = get_MetEireann.fetch_parse_data()
# print(weather_data)
# create_weather_image(weather_data, img, draw, font)


# # Plot the tide data
# plt.figure(figsize=(12, 6))
# plot_tide_data(df_historical, 'Historical Tide Level (LAT)', 'blue')
# plot_tide_data(df_predicted, 'Predicted Tide Level (LAT)', 'red')
# plot_tide_data(df_merged, 'Merged Tide Level (LAT)', 'green')
# plt.xlabel('Time')
# plt.ylabel('Tide Level (m relative to LAT)')
# plt.title('Tide Level Over Time (Sligo Station)')
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show()


