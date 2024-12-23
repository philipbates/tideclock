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
    
# Function to plot tide data
def plot_tide_data(df, label, color):
    plt.plot(df['time'], df['tide_level'], label=label, color=color)

def draw_point(draw, ptx, pty, radius):
    ptradius = radius
    draw.ellipse((ptx - ptradius, pty - ptradius, ptx + ptradius, pty + ptradius), fill='black')
    ptradius = min(1, radius - 2)
    draw.ellipse((ptx - ptradius, pty - ptradius, ptx + ptradius, pty + ptradius), fill='white')

# Function to create and save tide plot image
def create_tide_plot_image(df, filename):
    
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
    time_lower_limit_24hr = current_time - 12 * 60 * 60
    time_upper_limit_24hr = current_time + 12 * 60 * 60
    time_lower_limit_full = current_time - 6 * 24 * 60 * 60
    time_upper_limit_full = current_time + 6 * 24 * 60 * 60
    tide_upper_limit =  2
    tide_lower_limit = -2
    time_span_24hr = [time_lower_limit_24hr, time_upper_limit_24hr]
    time_span_full = [time_lower_limit_full, time_upper_limit_full]
    tide_span = [tide_lower_limit, tide_upper_limit]


    # get the tide data
    water_levels = df['tide_level'].values
    water_levels_smooth = df['tide_level'].rolling(window=15, center=True).mean().values

    # plot in the area Y 0 to 80 all the predicted data
    # plot in the area Y 80 to 320 only the data for the current 24 hrs
    px_for_weather = (0, 800, 0, 80)
    px_for_24hr = (0, 800, 100, 300)
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
    past_water_levels = water_levels_smooth[(timestamps >= time_span_24hr[0]) & (timestamps <= current_time)]
    future_times = timestamps[(timestamps > current_time) & (timestamps <= time_span_24hr[1])]
    future_water_levels = water_levels_smooth[(timestamps > current_time) & (timestamps <= time_span_24hr[1])]


    x_px_24r, y_px_24hr = mapper_24hr.map_vectors(timestamps24hr, tide_24hr)
    points = list(zip(x_px_24r, y_px_24hr ))
    draw.polygon([(0, 480)] + points + [(800, 480)], fill='lightgrey')
    
    # Draw a solid line for the water level at all timestamps up to the present time

    x_normalized, y_normalized = mapper_24hr.map_vectors(past_times, past_water_levels)
    points = list(zip(x_normalized, y_normalized))
    draw.line(points, fill='black', width=2)
    
    # Mark the current time with a sphere
    ptx, pty = mapper_24hr.map_point(pt_now)
    draw_point(draw, ptx, pty, radius=4)

    
    # Find next Future high and low tide
    max_index = np.argmax(future_water_levels)
    min_index = np.argmin(future_water_levels)
    HighTidexy = [future_times[max_index], future_water_levels[max_index]]
    LowTidexy = [future_times[min_index], future_water_levels[min_index]]
    print(f'High tide index: {max_index}, Low tide index: {min_index}')
    print(f'High tide time: {datetime.fromtimestamp(future_times[max_index], timezone.utc)}')
    HighTidex, HighTidey = mapper_24hr.map_point(HighTidexy)
    LowTidex, LowTidey = mapper_24hr.map_point(LowTidexy)

    #draw vertical lines for high and low tide
    draw.line((HighTidex, HighTidey, HighTidex, HighTidey + 50), fill='black')
    draw.line((LowTidex, LowTidey, LowTidex, LowTidey - 50), fill='black')
    
    font = ImageFont.truetype("Work-Sans-1.50/fonts/webfonts/ttf/WorkSans-Medium.ttf", size=32)
    # draw points and text for high tide
    draw_point(draw, HighTidex, HighTidey, 4)
    label_time = datetime.fromtimestamp(future_times[max_index], timezone.utc).strftime('%H:%M')
    draw.text((HighTidex, LowTidey+5), label_time, fill='black', font=font, anchor='ms')
    print(f"High tide time: {label_time} located at {HighTidex, HighTidey}")
    
    # draw points and text for low tide
    draw_point(draw, LowTidex, LowTidey, 4)
    label_time = datetime.fromtimestamp(future_times[min_index], timezone.utc).strftime('%H:%M')
    draw.text((LowTidex, HighTidey-5), label_time, fill='black', font=font, anchor='mt')
    print(f'Low tide time: {datetime.fromtimestamp(future_times[min_index], timezone.utc)}')

    #################################################################################
    ####### full historical + predicted data plot #######
    #################################################################################
    timestamps_full = timestamps[(timestamps >= time_span_full[0]) & (timestamps <= time_span_full[1])]
    tide_full = water_levels[(timestamps >= time_span_full[0]) & (timestamps <= time_span_full[1])]
    x_normalized, y_normalized = mapper_full.map_vectors(timestamps, water_levels)
    points = list(zip(x_normalized, y_normalized))
    draw.polygon([(0, 480)] + points + [(800, 480)], fill='black')
    
    # Mark the current time with a sphere
    ptx, pty = mapper_full.map_point(pt_now)
    draw_point(draw, ptx, pty, 4)
    window24hr_low = mapper_full.map_point([time_lower_limit_24hr, pty])
    window24hr_high = mapper_full.map_point([time_upper_limit_24hr, pty])


    # Mark boundaries of tide data
    draw.line((0, px_for_full[2], 800, px_for_full[2]), fill='black')
    draw.line((0, 400, 800, 400), fill='black')
    draw.line((0, px_for_full[3], 800, px_for_full[3]), fill='white')
   


    # font = ImageFont.load_default()
    # time_labels = [x_min, x_min + 0.25 * (x_max - x_min), x_min + 0.75 * (x_max - x_min), x_max]
    # for i, label in enumerate(time_labels):
    #     label_time = datetime.utcfromtimestamp(label).strftime('%Y-%m-%d %H:%M:%S')
    #     draw.text((i * 200, 400), label_time, fill='black', font=font)
    img.save(filename)
    img.show()
    return img, draw, font

def create_weather_image(weather_data, img, draw, font):
    # Draw the weather data
    for i, (time, data) in enumerate(weather_data.items()):
        draw.text((10, 10 + i * 20), f"{time}: {data['symbol']} {data['precipitation_mm']}mm", fill='black', font=font)

    # Save and display the image
    img.save('weather_plot.png')
    img.show()

# print("Fetching data from Met Éireann...")
# url = "http://openaccess.pf.api.met.ie/metno-wdb2ts/locationforecast"
# params = {
#     'lat': 54.4044,
#     'long': -8.5602
#     # 'from': '2024-12-15T00:00',
#     # 'to': '2024-12-15T00:00'
# }

# response = requests.get(url, params=params)
# print(f"Request URL: {response.url}")
# if response.status_code == 200:
#     with open('met_eireann_data.xml', 'wb') as file:
#         file.write(response.content)
#     print("Data downloaded successfully.")
# else:
#     print(f"Failed to download data. Status code: {response.status_code}")




# Main function
#################################################################################
####### Tide Data ##########
# Get tide data from the ERDP open data website of the marine institute
df_historical, df_predicted = get_TideData.fetch_and_format_tide_data()

# merge the dataframes on time, starting from the end of the historical data only
df_predicted_cut = df_predicted[df_predicted['time'] > df_historical['time'].max()]
df_historical_cut = df_historical[df_historical['time'] < df_predicted_cut['time'].min()]
df_merged = pd.concat([df_historical_cut, df_predicted_cut])
img, draw, font = create_tide_plot_image(df_merged, 'tide_plot.png')



#################################################################################
####### Weather Data ##########
time_now = datetime.now(timezone.utc)
# Get weather data from the Met Eireann website
weather_data = get_MetEireann.fetch_parse_data()
print(weather_data)
create_weather_image(weather_data, img, draw, font)


# Plot the tide data
plt.figure(figsize=(12, 6))
plot_tide_data(df_historical, 'Historical Tide Level (LAT)', 'blue')
plot_tide_data(df_predicted, 'Predicted Tide Level (LAT)', 'red')
# plot_tide_data(df_merged, 'Merged Tide Level (LAT)', 'green')
plt.xlabel('Time')
plt.ylabel('Tide Level (m relative to LAT)')
plt.title('Tide Level Over Time (Sligo Station)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


