import requests
from PIL import Image
import os
from PIL import ImageDraw, ImageFont

def download_met_eireann_data(from_date, to_date):
    url = "http://openaccess.pf.api.met.ie/metno-wdb2ts/locationforecast"
    params = {
        'lat': 54.4044,
        'long': -8.5602
        # 'from': '2024-12-15T00:00',
        # 'to': '2024-12-15T00:00'
    }
    
    response = requests.get(url, params=params)
    print(f"Request URL: {response.url}")
    if response.status_code == 200:
        with open('met_eireann_data.xml', 'wb') as file:
            file.write(response.content)
        print("Data downloaded successfully.")
    else:
        print(f"Failed to download data. Status code: {response.status_code}")
    return response


import xml.etree.ElementTree as ET



# Function to parse XML and extract specific values
def extract_weather_data(xml_string, start_time, end_time, elements_to_extract):
    # Parse the XML string
    root = ET.fromstring(xml_string)
    
    # Navigate to the product section where forecast data is stored
    product = root.find('product')
    
    # Iterate through each time element and extract data
    for time_element in product.findall('time'):
        from_time = time_element.get('from')
        to_time = time_element.get('to')
        
        # Check if the current time is within the specified range
        if from_time >= start_time and to_time <= end_time:
            location = time_element.find('location')
            precipitation = location.find('precipitation')
            
            # Only proceed if there is precipitation data
            if precipitation is not None:
                data_extracted = {}
                
                # Check for each requested element and gather data
                for element in elements_to_extract:
                    if element == 'symbol':
                        symbol = location.find('symbol')
                        if symbol is not None:
                            data_extracted['symbol'] = symbol.get('id')
                    if element == 'precipitation':
                        data_extracted['precipitation_mm'] = precipitation.get('value')
                        data_extracted['precipitation_probability'] = precipitation.get('probability')
                
                # Print the extracted data
                print(f"Data from {from_time} to {to_time}: {data_extracted}")

                weather_data = {}

                for time_element in product.findall('time'):
                    from_time = time_element.get('from')
                    to_time = time_element.get('to')

                    if from_time >= start_time and to_time <= end_time:
                        location = time_element.find('location')
                        precipitation = location.find('precipitation')

                        if precipitation is not None:
                            data_extracted = {}

                            for element in elements_to_extract:
                                if element == 'symbol':
                                    symbol = location.find('symbol')
                                    if symbol is not None:
                                        data_extracted['symbol'] = symbol.get('id')
                                if element == 'precipitation':
                                    data_extracted['precipitation_mm'] = precipitation.get('value')
                                    data_extracted['precipitation_probability'] = precipitation.get('probability')

                            weather_data[from_time] = data_extracted

                return weather_data
            

from_date = "2024-12-15T00:00"
to_date = "2024-12-17T23:00"
response = download_met_eireann_data(from_date, to_date)
# Specify the time range and elements to extract
start_time = from_date
end_time = to_date
elements_to_extract = ['symbol', 'precipitation']
xml_data = response.content.decode('utf-8')
print(xml_data)

# Call the function
weather_data = extract_weather_data(xml_data, start_time, end_time, elements_to_extract)

#print the number of items in the dictionary
print(len(weather_data))

#%%

# Define the mapping of weather symbols to font icons
symbol_to_icon = {
        "Error": "wi-na",
        "Sun": "wi-day-sunny",
        "LightCloud": "wi-day-cloudy",
        "PartlyCloud": "wi-day-cloudy-high",
        "Cloud": "wi-cloudy",
        "LightRainSun": "wi-day-rain",
        "LightRainThunderSun": "wi-day-storm-showers",
        "SleetSun": "wi-day-sleet",
        "SnowSun": "wi-day-snow",
        "LightRain": "wi-rain",
        "Rain": "wi-rain",
        "RainThunder": "wi-thunderstorm",
        "Sleet": "wi-sleet",
        "Snow": "wi-snow",
        "SnowThunder": "wi-snow-thunderstorm",
        "Fog": "wi-fog",
        "SleetSunThunder": "wi-day-sleet-storm",
        "SnowSunThunder": "wi-day-snow-thunderstorm",
        "LightRainThunder": "wi-storm-showers",
        "SleetThunder": "wi-sleet-storm",
        "DrizzleThunderSun": "wi-day-showers",
        "RainThunderSun": "wi-day-thunderstorm",
        "LightSleetThunderSun": "wi-day-sleet-storm",
        "HeavySleetThunderSun": "wi-day-sleet-storm",
        "LightSnowThunderSun": "wi-day-snow-thunderstorm",
        "HeavySnowThunderSun": "wi-day-snow-thunderstorm",
        "DrizzleThunder": "wi-storm-showers",
        "LightSleetThunder": "wi-sleet-storm",
        "HeavySleetThunder": "wi-sleet-storm",
        "LightSnowThunder": "wi-snow-thunderstorm",
        "HeavySnowThunder": "wi-snow-thunderstorm",
        "DrizzleSun": "wi-day-sprinkle",
        "RainSun": "wi-day-rain",
        "LightSleetSun": "wi-day-sleet",
        "HeavySleetSun": "wi-day-sleet",
        "LightSnowSun": "wi-day-snow",
        "HeavySnowSun": "wi-day-snow",
        "Drizzle": "wi-sprinkle",
        "LightSleet": "wi-sleet",
        "HeavySleet": "wi-sleet",
        "LightSnow": "wi-snow",
        "HeavySnow": "wi-snow"
    }

# using the dict above, print the weather for the next 24 hours naming both the met eireann symbol and the font icon
# for time, info in weather_data.items():
#     symbol = info.get('symbol', 'unknown')
#     precipitation_mm = info.get('precipitation_mm', 'unknown')
#     precipitation_probability = info.get('precipitation_probability', 'unknown')
#     icon = info.get('symbol', 'unknown')
#     print(f"{time}: {symbol} {icon} Precipitation: {precipitation_mm}mm Probability: {precipitation_probability}%")
    
print('---------------------- symbols --------------------')
def create_weather_image(weather_data, output_path, icon_dir, symbol_to_icon):
    img_width = 800
    img_height = 480
    icon_size = (80, 80)
    img = Image.new('RGBA', (img_width, img_height), color='white')
    tidepath = "/Users/philipkevinbates/Documents/Coding/Tides/tide_plot.png"
    img = Image.open(tidepath).convert('RGBA')

    for i, (time, info) in enumerate(weather_data.items()):
        if i >= 10:
            break
        symbol = info.get('symbol', 'unknown')
        icon_name = symbol_to_icon.get(symbol, 'wi-na')
        png_path = os.path.join(icon_dir, f"{icon_name}.png")
        icon_img = Image.open(png_path).convert('RGBA')
        #display the image
        print(f"{time}: {symbol} {png_path}")
        
        # Resize the icon image
        icon_img = icon_img.resize(icon_size)
        # icon_img.show()
        img.paste(icon_img, (i * icon_size[0], 0))
        # img.show()
        # Draw the precipitation probability below the icon
        precipitation_probability = info.get('precipitation_probability', 'unknown')
        if precipitation_probability != 'unknown':
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            text_position = (i * icon_size[0]+30, icon_size[1] + 10)
            draw.text(text_position, f"{precipitation_probability}%", fill="black", font=font)
        #close the displayed image
        # icon_img.show()
        img.show()
    img.save(output_path)
        

icon_dir = "/Users/philipkevinbates/Documents/Coding/Tides/weather-icons-png"
output_path = "/Users/philipkevinbates/Documents/Coding/Tides/weather_forecast.png"
create_weather_image(weather_data, output_path, icon_dir, symbol_to_icon)


# ###### Met Eireann Weather Symbols ######
# # Define the table data as a list of tuples (description, daytime_number, [optional] nighttime_number)
# met_symbols_data = [
#     ("Error", 0),
#     ("Sun", 1, 101),
#     ("LightCloud", 2, 102),
#     ("PartlyCloud", 3, 103),
#     ("Cloud", 4),
#     ("LightRainSun", 5, 105),
#     ("LightRainThunderSun", 6, 106),
#     ("SleetSun", 7, 107),
#     ("SnowSun", 8, 108),
#     ("LightRain", 9),
#     ("Rain", 10),
#     ("RainThunder", 11),
#     ("Sleet", 12),
#     ("Snow", 13),
#     ("SnowThunder", 14),
#     ("Fog", 15),
#     ("SleetSunThunder", 20, 120),
#     ("SnowSunThunder", 21, 121),
#     ("LightRainThunder", 22),
#     ("SleetThunder", 23),
#     ("DrizzleThunderSun", 24, 124),
#     ("RainThunderSun", 25, 125),
#     ("LightSleetThunderSun", 26, 126),
#     ("HeavySleetThunderSun", 27, 127),
#     ("LightSnowThunderSun", 28, 128),
#     ("HeavySnowThunderSun", 29, 129),
#     ("DrizzleThunder", 30),
#     ("LightSleetThunder", 31),
#     ("HeavySleetThunder", 32),
#     ("LightSnowThunder", 33),
#     ("HeavySnowThunder", 34),
#     ("DrizzleSun", 40, 140),
#     ("RainSun", 41, 141),
#     ("LightSleetSun", 42, 142),
#     ("HeavySleetSun", 43, 143),
#     ("LightSnowSun", 44, 144),
#     ("HeavySnowSun", 45, 145),
#     ("Drizzle", 46),
#     ("LightSleet", 47),
#     ("HeavySleet", 48),
#     ("LightSnow", 49),
#     ("HeavySnow", 50)
# ]


'''
# THisis a list of all possible weather icons
#{content:"\f00d"}.wi-day-cloudy:before{content:"\f002"}.wi-day-cloudy-gusts:before{content:"\f000"}.wi-day-cloudy-windy:before{content:"\f001"}.wi-day-fog:before{content:"\f003"}.wi-day-hail:before{content:"\f004"}.wi-day-haze:before{content:"\f0b6"}.wi-day-lightning:before{content:"\f005"}.wi-day-rain:before{content:"\f008"}.wi-day-rain-mix:before{content:"\f006"}.wi-day-rain-wind:before{content:"\f007"}.wi-day-showers:before{content:"\f009"}.wi-day-sleet:before{content:"\f0b2"}.wi-day-sleet-storm:before{content:"\f068"}.wi-day-snow:before{content:"\f00a"}.wi-day-snow-thunderstorm:before{content:"\f06b"}.wi-day-snow-wind:before{content:"\f065"}.wi-day-sprinkle:before{content:"\f00b"}.wi-day-storm-showers:before{content:"\f00e"}.wi-day-sunny-overcast:before{content:"\f00c"}.wi-day-thunderstorm:before{content:"\f010"}.wi-day-windy:before{content:"\f085"}.wi-solar-eclipse:before{content:"\f06e"}.wi-hot:before{content:"\f072"}.wi-day-cloudy-high:before{content:"\f07d"}.wi-day-light-wind:before{content:"\f0c4"}.wi-night-clear:before{content:"\f02e"}.wi-night-alt-cloudy:before{content:"\f086"}.wi-night-alt-cloudy-gusts:before{content:"\f022"}.wi-night-alt-cloudy-windy:before{content:"\f023"}.wi-night-alt-hail:before{content:"\f024"}.wi-night-alt-lightning:before{content:"\f025"}.wi-night-alt-rain:before{content:"\f028"}.wi-night-alt-rain-mix:before{content:"\f026"}.wi-night-alt-rain-wind:before{content:"\f027"}.wi-night-alt-showers:before{content:"\f029"}.wi-night-alt-sleet:before{content:"\f0b4"}.wi-night-alt-sleet-storm:before{content:"\f06a"}.wi-night-alt-snow:before{content:"\f02a"}.wi-night-alt-snow-thunderstorm:before{content:"\f06d"}.wi-night-alt-snow-wind:before{content:"\f067"}.wi-night-alt-sprinkle:before{content:"\f02b"}.wi-night-alt-storm-showers:before{content:"\f02c"}.wi-night-alt-thunderstorm:before{content:"\f02d"}.wi-night-cloudy:before{content:"\f031"}.wi-night-cloudy-gusts:before{content:"\f02f"}.wi-night-cloudy-windy:before{content:"\f030"}.wi-night-fog:before{content:"\f04a"}.wi-night-hail:before{content:"\f032"}.wi-night-lightning:before{content:"\f033"}.wi-night-partly-cloudy:before{content:"\f083"}.wi-night-rain:before{content:"\f036"}.wi-night-rain-mix:before{content:"\f034"}.wi-night-rain-wind:before{content:"\f035"}.wi-night-showers:before{content:"\f037"}.wi-night-sleet:before{content:"\f0b3"}.wi-night-sleet-storm:before{content:"\f069"}.wi-night-snow:before{content:"\f038"}.wi-night-snow-thunderstorm:before{content:"\f06c"}.wi-night-snow-wind:before{content:"\f066"}.wi-night-sprinkle:before{content:"\f039"}.wi-night-storm-showers:before{content:"\f03a"}.wi-night-thunderstorm:before{content:"\f03b"}.wi-lunar-eclipse:before{content:"\f070"}.wi-stars:before{content:"\f077"}.wi-storm-showers:before{content:"\f01d"}.wi-thunderstorm:before{content:"\f01e"}.wi-night-alt-cloudy-high:before{content:"\f07e"}.wi-night-cloudy-high:before{content:"\f080"}.wi-night-alt-partly-cloudy:before{content:"\f081"}.wi-cloud:before{content:"\f041"}.wi-cloudy:before{content:"\f013"}.wi-cloudy-gusts:before{content:"\f011"}.wi-cloudy-windy:before{content:"\f012"}.wi-fog:before{content:"\f014"}.wi-hail:before{content:"\f015"}.wi-rain:before{content:"\f019"}.wi-rain-mix:before{content:"\f017"}.wi-rain-wind:before{content:"\f018"}.wi-showers:before{content:"\f01a"}.wi-sleet:before{content:"\f0b5"}.wi-snow:before{content:"\f01b"}.wi-sprinkle:before{content:"\f01c"}.wi-storm-showers:before{content:"\f01d"}.wi-thunderstorm:before{content:"\f01e"}.wi-snow-wind:before{content:"\f064"}.wi-snow:before{content:"\f01b"}.wi-smog:before{content:"\f074"}.wi-smoke:before{content:"\f062"}.wi-lightning:before{content:"\f016"}.wi-raindrops:before{content:"\f04e"}.wi-raindrop:before{content:"\f078"}.wi-dust:before{content:"\f063"}.wi-snowflake-cold:before{content:"\f076"}.wi-windy:before{content:"\f021"}.wi-strong-wind:before{content:"\f050"}.wi-sandstorm:before{content:"\f082"}.wi-earthquake:before{content:"\f0c6"}.wi-fire:before{content:"\f0c7"}.wi-flood:before{content:"\f07c"}.wi-meteor:before{content:"\f071"}.wi-tsunami:before{content:"\f0c5"}.wi-volcano:before{content:"\f0c8"}.wi-hurricane:before{content:"\f073"}.wi-tornado:before{content:"\f056"}.wi-small-craft-advisory:before{content:"\f0cc"}.wi-gale-warning:before{content:"\f0cd"}.wi-storm-warning:before{content:"\f0ce"}.wi-hurricane-warning:before{content:"\f0cf"}.wi-wind-direction:before{content:"\f0b1"}.wi-alien:before{content:"\f075"}.wi-celsius:before{content:"\f03c"}.wi-fahrenheit:before{content:"\f045"}.wi-degrees:before{content:"\f042"}.wi-thermometer:before{content:"\f055"}.wi-thermometer-exterior:before{content:"\f053"}.wi-thermometer-internal:before{content:"\f054"}.wi-cloud-down:before{content:"\f03d"}.wi-cloud-up:before{content:"\f040"}.wi-cloud-refresh:before{content:"\f03e"}.wi-horizon:before{content:"\f047"}.wi-horizon-alt:before{content:"\f046"}.wi-sunrise:before{content:"\f051"}.wi-sunset:before{content:"\f052"}.wi-moonrise:before{content:"\f0c9"}.wi-moonset:before{content:"\f0ca"}.wi-refresh:before{content:"\f04c"}.wi-refresh-alt:before{content:"\f04b"}.wi-umbrella:before{content:"\f084"}.wi-barometer:before{content:"\f079"}.wi-humidity:before{content:"\f07a"}.wi-na:before{content:"\f07b"}.wi-train:before{content:"\f0cb"}.wi-moon-new:before{content:"\f095"}.wi-moon-waxing-crescent-1:before{content:"\f096"}.wi-moon-waxing-crescent-2:before{content:"\f097"}.wi-moon-waxing-crescent-3:before{content:"\f098"}.wi-moon-waxing-crescent-4:before{content:"\f099"}.wi-moon-waxing-crescent-5:before{content:"\f09a"}.wi-moon-waxing-crescent-6:before{content:"\f09b"}.wi-moon-first-quarter:before{content:"\f09c"}.wi-moon-waxing-gibbous-1:before{content:"\f09d"}.wi-moon-waxing-gibbous-2:before{content:"\f09e"}.wi-moon-waxing-gibbous-3:before{content:"\f09f"}.wi-moon-waxing-gibbous-4:before{content:"\f0a0"}.wi-moon-waxing-gibbous-5:before{content:"\f0a1"}.wi-moon-waxing-gibbous-6:before{content:"\f0a2"}.wi-moon-full:before{content:"\f0a3"}.wi-moon-waning-gibbous-1:before{content:"\f0a4"}.wi-moon-waning-gibbous-2:before{content:"\f0a5"}.wi-moon-waning-gibbous-3:before{content:"\f0a6"}.wi-moon-waning-gibbous-4:before{content:"\f0a7"}.wi-moon-waning-gibbous-5:before{content:"\f0a8"}.wi-moon-waning-gibbous-6:before{content:"\f0a9"}.wi-moon-third-quarter:before{content:"\f0aa"}.wi-moon-waning-crescent-1:before{content:"\f0ab"}.wi-moon-waning-crescent-2:before{content:"\f0ac"}.wi-moon-waning-crescent-3:before{content:"\f0ad"}.wi-moon-waning-crescent-4:before{content:"\f0ae"}.wi-moon-waning-crescent-5:before{content:"\f0af"}.wi-moon-waning-crescent-6:before{content:"\f0b0"}.wi-moon-alt-new:before{content:"\f0eb"}.wi-moon-alt-waxing-crescent-1:before{content:"\f0d0"}.wi-moon-alt-waxing-crescent-2:before{content:"\f0d1"}.wi-moon-alt-waxing-crescent-3:before{content:"\f0d2"}.wi-moon-alt-waxing-crescent-4:before{content:"\f0d3"}.wi-moon-alt-waxing-crescent-5:before{content:"\f0d4"}.wi-moon-alt-waxing-crescent-6:before{content:"\f0d5"}.wi-moon-alt-first-quarter:before{content:"\f0d6"}.wi-moon-alt-waxing-gibbous-1:before{content:"\f0d7"}.wi-moon-alt-waxing-gibbous-2:before{content:"\f0d8"}.wi-moon-alt-waxing-gibbous-3:before{content:"\f0d9"}.wi-moon-alt-waxing-gibbous-4:before{content:"\f0da"}.wi-moon-alt-waxing-gibbous-5:before{content:"\f0db"}.wi-moon-alt-waxing-gibbous-6:before{content:"\f0dc"}.wi-moon-alt-full:before{content:"\f0dd"}.wi-moon-alt-waning-gibbous-1:before{content:"\f0de"}.wi-moon-alt-waning-gibbous-2:before{content:"\f0df"}.wi-moon-alt-waning-gibbous-3:before{content:"\f0e0"}.wi-moon-alt-waning-gibbous-4:before{content:"\f0e1"}.wi-moon-alt-waning-gibbous-5:before{content:"\f0e2"}.wi-moon-alt-waning-gibbous-6:before{content:"\f0e3"}.wi-moon-alt-third-quarter:before{content:"\f0e4"}.wi-moon-alt-waning-crescent-1:before{content:"\f0e5"}.wi-moon-alt-waning-crescent-2:before{content:"\f0e6"}.wi-moon-alt-waning-crescent-3:before{content:"\f0e7"}.wi-moon-alt-waning-crescent-4:before{content:"\f0e8"}.wi-moon-alt-waning-crescent-5:before{content:"\f0e9"}.wi-moon-alt-waning-crescent-6:before{content:"\f0ea"}.wi-moon-0:before{content:"\f095"}.wi-moon-1:before{content:"\f096"}.wi-moon-2:before{content:"\f097"}.wi-moon-3:before{content:"\f098"}.wi-moon-4:before{content:"\f099"}.wi-moon-5:before{content:"\f09a"}.wi-moon-6:before{content:"\f09b"}.wi-moon-7:before{content:"\f09c"}.wi-moon-8:before{content:"\f09d"}.wi-moon-9:before{content:"\f09e"}.wi-moon-10:before{content:"\f09f"}.wi-moon-11:before{content:"\f0a0"}.wi-moon-12:before{content:"\f0a1"}.wi-moon-13:before{content:"\f0a2"}.wi-moon-14:before{content:"\f0a3"}.wi-moon-15:before{content:"\f0a4"}.wi-moon-16:before{content:"\f0a5"}.wi-moon-17:before{content:"\f0a6"}.wi-moon-18:before{content:"\f0a7"}.wi-moon-19:before{content:"\f0a8"}.wi-moon-20:before{content:"\f0a9"}.wi-moon-21:before{content:"\f0aa"}.wi-moon-22:before{content:"\f0ab"}.wi-moon-23:before{content:"\f0ac"}.wi-moon-24:before{content:"\f0ad"}.wi-moon-25:before{content:"\f0ae"}.wi-moon-26:before{content:"\f0af"}.wi-moon-27:before{content:"\f0b0"}.wi-time-1:before{content:"\f08a"}.wi-time-2:before{content:"\f08b"}.wi-time-3:before{content:"\f08c"}.wi-time-4:before{content:"\f08d"}.wi-time-5:before{content:"\f08e"}.wi-time-6:before{content:"\f08f"}.wi-time-7:before{content:"\f090"}.wi-time-8:before{content:"\f091"}.wi-time-9:before{content:"\f092"}.wi-time-10:before{content:"\f093"}.wi-time-11:before{content:"\f094"}.wi-time-12:before{content:"\f089"}.wi-direction-up:before{content:"\f058"}.wi-direction-up-right:before{content:"\f057"}.wi-direction-right:before{content:"\f04d"}.wi-direction-down-right:before{content:"\f088"}.wi-direction-down:before{content:"\f044"}.wi-direction-down-left:before{content:"\f043"}.wi-direction-left:before{content:"\f048"}.wi-direction-up-left:before{content:"\f087"}.wi-wind-beaufort-0:before{content:"\f0b7"}.wi-wind-beaufort-1:before{content:"\f0b8"}.wi-wind-beaufort-2:before{content:"\f0b9"}.wi-wind-beaufort-3:before{content:"\f0ba"}.wi-wind-beaufort-4:before{content:"\f0bb"}.wi-wind-beaufort-5:before{content:"\f0bc"}.wi-wind-beaufort-6:before{content:"\f0bd"}.wi-wind-beaufort-7:before{content:"\f0be"}.wi-wind-beaufort-8:before{content:"\f0bf"}.wi-wind-beaufort-9:before{content:"\f0c0"}.wi-wind-beaufort-10:before{content:"\f0c1"}.wi-wind-beaufort-11:before{content:"\f0c2"}.wi-wind-beaufort-12:before{content:"\f0c3"}.wi-yahoo-0:before{content:"\f056"}.wi-yahoo-1:before{content:"\f00e"}.wi-yahoo-2:before{content:"\f073"}.wi-yahoo-3:before{content:"\f01e"}.wi-yahoo-4:before{content:"\f01e"}.wi-yahoo-5:before{content:"\f017"}.wi-yahoo-6:before{content:"\f017"}.wi-yahoo-7:before{content:"\f017"}.wi-yahoo-8:before{content:"\f015"}.wi-yahoo-9:before{content:"\f01a"}.wi-yahoo-10:before{content:"\f015"}.wi-yahoo-11:before{content:"\f01a"}.wi-yahoo-12:before{content:"\f01a"}.wi-yahoo-13:before{content:"\f01b"}.wi-yahoo-14:before{content:"\f00a"}.wi-yahoo-15:before{content:"\f064"}.wi-yahoo-16:before{content:"\f01b"}.wi-yahoo-17:before{content:"\f015"}.wi-yahoo-18:before{content:"\f017"}.wi-yahoo-19:before{content:"\f063"}.wi-yahoo-20:before{content:"\f014"}.wi-yahoo-21:before{content:"\f021"}.wi-yahoo-22:before{content:"\f062"}.wi-yahoo-23:before{content:"\f050"}.wi-yahoo-24:before{content:"\f050"}.wi-yahoo-25:before{content:"\f076"}.wi-yahoo-26:before{content:"\f013"}.wi-yahoo-27:before{content:"\f031"}.wi-yahoo-28:before{content:"\f002"}.wi-yahoo-29:before{content:"\f031"}.wi-yahoo-30:before{content:"\f002"}.wi-yahoo-31:before{content:"\f02e"}.wi-yahoo-32:before{content:"\f00d"}.wi-yahoo-33:before{content:"\f083"}.wi-yahoo-34:before{content:"\f00c"}.wi-yahoo-35:before{content:"\f017"}.wi-yahoo-36:before{content:"\f072"}.wi-yahoo-37:before{content:"\f00e"}.wi-yahoo-38:before{content:"\f00e"}.wi-yahoo-39:before{content:"\f00e"}.wi-yahoo-40:before{content:"\f01a"}.wi-yahoo-41:before{content:"\f064"}.wi-yahoo-42:before{content:"\f01b"}.wi-yahoo-43:before{content:"\f064"}.wi-yahoo-44:before{content:"\f00c"}.wi-yahoo-45:before{content:"\f00e"}.wi-yahoo-46:before{content:"\f01b"}.wi-yahoo-47:before{content:"\f00e"}.wi-yahoo-3200:before{content:"\f077"}.wi-forecast-io-clear-day:before{content:"\f00d"}.wi-forecast-io-clear-night:before{content:"\f02e"}.wi-forecast-io-rain:before{content:"\f019"}.wi-forecast-io-snow:before{content:"\f01b"}.wi-forecast-io-sleet:before{content:"\f0b5"}.wi-forecast-io-wind:before{content:"\f050"}.wi-forecast-io-fog:before{content:"\f014"}.wi-forecast-io-cloudy:before{content:"\f013"}.wi-forecast-io-partly-cloudy-day:before{content:"\f002"}.wi-forecast-io-partly-cloudy-night:before{content:"\f031"}.wi-forecast-io-hail:before{content:"\f015"}.wi-forecast-io-thunderstorm:before{content:"\f01e"}.wi-forecast-io-tornado:before{content:"\f056"}.wi-wmo4680-0:before,.wi-wmo4680-00:before{content:"\f055"}.wi-wmo4680-1:before,.wi-wmo4680-01:before{content:"\f013"}.wi-wmo4680-2:before,.wi-wmo4680-02:before{content:"\f055"}.wi-wmo4680-3:before,.wi-wmo4680-03:before{content:"\f013"}.wi-wmo4680-4:before,.wi-wmo4680-04:before{content:"\f014"}.wi-wmo4680-5:before,.wi-wmo4680-05:before{content:"\f014"}.wi-wmo4680-10:before{content:"\f014"}.wi-wmo4680-11:before{content:"\f014"}.wi-wmo4680-12:before{content:"\f016"}.wi-wmo4680-18:before{content:"\f050"}.wi-wmo4680-20:before{content:"\f014"}.wi-wmo4680-21:before{content:"\f017"}.wi-wmo4680-22:before{content:"\f017"}.wi-wmo4680-23:before{content:"\f019"}.wi-wmo4680-24:before{content:"\f01b"}.wi-wmo4680-25:before{content:"\f015"}.wi-wmo4680-26:before{content:"\f01e"}.wi-wmo4680-27:before{content:"\f063"}.wi-wmo4680-28:before{content:"\f063"}.wi-wmo4680-29:before{content:"\f063"}.wi-wmo4680-30:before{content:"\f014"}.wi-wmo4680-31:before{content:"\f014"}.wi-wmo4680-32:before{content:"\f014"}.wi-wmo4680-33:before{content:"\f014"}.wi-wmo4680-34:before{content:"\f014"}.wi-wmo4680-35:before{content:"\f014"}.wi-wmo4680-40:before{content:"\f017"}.wi-wmo4680-41:before{content:"\f01c"}.wi-wmo4680-42:before{content:"\f019"}.wi-wmo4680-43:before{content:"\f01c"}.wi-wmo4680-44:before{content:"\f019"}.wi-wmo4680-45:before{content:"\f015"}.wi-wmo4680-46:before{content:"\f015"}.wi-wmo4680-47:before{content:"\f01b"}.wi-wmo4680-48:before{content:"\f01b"}.wi-wmo4680-50:before{content:"\f01c"}.wi-wmo4680-51:before{content:"\f01c"}.wi-wmo4680-52:before{content:"\f019"}.wi-wmo4680-53:before{content:"\f019"}.wi-wmo4680-54:before{content:"\f076"}.wi-wmo4680-55:before{content:"\f076"}.wi-wmo4680-56:before{content:"\f076"}.wi-wmo4680-57:before{content:"\f01c"}.wi-wmo4680-58:before{content:"\f019"}.wi-wmo4680-60:before{content:"\f01c"}.wi-wmo4680-61:before{content:"\f01c"}.wi-wmo4680-62:before{content:"\f019"}.wi-wmo4680-63:before{content:"\f019"}.wi-wmo4680-64:before{content:"\f015"}.wi-wmo4680-65:before{content:"\f015"}.wi-wmo4680-66:before{content:"\f015"}.wi-wmo4680-67:before{content:"\f017"}.wi-wmo4680-68:before{content:"\f017"}.wi-wmo4680-70:before{content:"\f01b"}.wi-wmo4680-71:before{content:"\f01b"}.wi-wmo4680-72:before{content:"\f01b"}.wi-wmo4680-73:before{content:"\f01b"}.wi-wmo4680-74:before{content:"\f076"}.wi-wmo4680-75:before{content:"\f076"}.wi-wmo4680-76:before{content:"\f076"}.wi-wmo4680-77:before{content:"\f01b"}.wi-wmo4680-78:before{content:"\f076"}.wi-wmo4680-80:before{content:"\f019"}.wi-wmo4680-81:before{content:"\f01c"}.wi-wmo4680-82:before{content:"\f019"}.wi-wmo4680-83:before{content:"\f019"}.wi-wmo4680-84:before{content:"\f01d"}.wi-wmo4680-85:before{content:"\f017"}.wi-wmo4680-86:before{content:"\f017"}.wi-wmo4680-87:before{content:"\f017"}.wi-wmo4680-89:before{content:"\f015"}.wi-wmo4680-90:before{content:"\f016"}.wi-wmo4680-91:before{content:"\f01d"}.wi-wmo4680-92:before{content:"\f01e"}.wi-wmo4680-93:before{content:"\f01e"}.wi-wmo4680-94:before{content:"\f016"}.wi-wmo4680-95:before{content:"\f01e"}.wi-wmo4680-96:before{content:"\f01e"}.wi-wmo4680-99:before{content:"\f056"}.wi-owm-200:before{content:"\f01e"}.wi-owm-201:before{content:"\f01e"}.wi-owm-202:before{content:"\f01e"}.wi-owm-210:before{content:"\f016"}.wi-owm-211:before{content:"\f016"}.wi-owm-212:before{content:"\f016"}.wi-owm-221:before{content:"\f016"}.wi-owm-230:before{content:"\f01e"}.wi-owm-231:before{content:"\f01e"}.wi-owm-232:before{content:"\f01e"}.wi-owm-300:before{content:"\f01c"}.wi-owm-301:before{content:"\f01c"}.wi-owm-302:before{content:"\f019"}.wi-owm-310:before{content:"\f017"}.wi-owm-311:before{content:"\f019"}.wi-owm-312:before{content:"\f019"}.wi-owm-313:before{content:"\f01a"}.wi-owm-314:before{content:"\f019"}.wi-owm-321:before{content:"\f01c"}.wi-owm-500:before{content:"\f01c"}.wi-owm-501:before{content:"\f019"}.wi-owm-502:before{content:"\f019"}.wi-owm-503:before{content:"\f019"}.wi-owm-504:before{content:"\f019"}.wi-owm-511:before{content:"\f017"}.wi-owm-520:before{content:"\f01a"}.wi-owm-521:before{content:"\f01a"}.wi-owm-522:before{content:"\f01a"}.wi-owm-531:before{content:"\f01d"}.wi-owm-600:before{content:"\f01b"}.wi-owm-601:before{content:"\f01b"}.wi-owm-602:before{content:"\f0b5"}.wi-owm-611:before{content:"\f017"}.wi-owm-612:before{content:"\f017"}.wi-owm-615:before{content:"\f017"}.wi-owm-616:before{content:"\f017"}.wi-owm-620:before{content:"\f017"}.wi-owm-621:before{content:"\f01b"}.wi-owm-622:before{content:"\f01b"}.wi-owm-701:before{content:"\f014"}.wi-owm-711:before{content:"\f062"}.wi-owm-721:before{content:"\f0b6"}.wi-owm-731:before{content:"\f063"}.wi-owm-741:before{content:"\f014"}.wi-owm-761:before{content:"\f063"}.wi-owm-762:before{content:"\f063"}.wi-owm-771:before{content:"\f011"}.wi-owm-781:before{content:"\f056"}.wi-owm-800:before{content:"\f00d"}.wi-owm-801:before{content:"\f041"}.wi-owm-802:before{content:"\f041"}.wi-owm-803:before{content:"\f013"}.wi-owm-804:before{content:"\f013"}.wi-owm-900:before{content:"\f056"}.wi-owm-901:before{content:"\f01d"}.wi-owm-902:before{content:"\f073"}.wi-owm-903:before{content:"\f076"}.wi-owm-904:before{content:"\f072"}.wi-owm-905:before{content:"\f021"}.wi-owm-906:before{content:"\f015"}.wi-owm-957:before{content:"\f050"}.wi-owm-day-200:before{content:"\f010"}.wi-owm-day-201:before{content:"\f010"}.wi-owm-day-202:before{content:"\f010"}.wi-owm-day-210:before{content:"\f005"}.wi-owm-day-211:before{content:"\f005"}.wi-owm-day-212:before{content:"\f005"}.wi-owm-day-221:before{content:"\f005"}.wi-owm-day-230:before{content:"\f010"}.wi-owm-day-231:before{content:"\f010"}.wi-owm-day-232:before{content:"\f010"}.wi-owm-day-300:before{content:"\f00b"}.wi-owm-day-301:before{content:"\f00b"}.wi-owm-day-302:before{content:"\f008"}.wi-owm-day-310:before{content:"\f008"}.wi-owm-day-311:before{content:"\f008"}.wi-owm-day-312:before{content:"\f008"}.wi-owm-day-313:before{content:"\f008"}.wi-owm-day-314:before{content:"\f008"}.wi-owm-day-321:before{content:"\f00b"}.wi-owm-day-500:before{content:"\f00b"}.wi-owm-day-501:before{content:"\f008"}.wi-owm-day-502:before{content:"\f008"}.wi-owm-day-503:before{content:"\f008"}.wi-owm-day-504:before{content:"\f008"}.wi-owm-day-511:before{content:"\f006"}.wi-owm-day-520:before{content:"\f009"}.wi-owm-day-521:before{content:"\f009"}.wi-owm-day-522:before{content:"\f009"}.wi-owm-day-531:before{content:"\f00e"}.wi-owm-day-600:before{content:"\f00a"}.wi-owm-day-601:before{content:"\f0b2"}.wi-owm-day-602:before{content:"\f00a"}.wi-owm-day-611:before{content:"\f006"}.wi-owm-day-612:before{content:"\f006"}.wi-owm-day-615:before{content:"\f006"}.wi-owm-day-616:before{content:"\f006"}.wi-owm-day-620:before{content:"\f006"}.wi-owm-day-621:before{content:"\f00a"}.wi-owm-day-622:before{content:"\f00a"}.wi-owm-day-701:before{content:"\f003"}.wi-owm-day-711:before{content:"\f062"}.wi-owm-day-721:before{content:"\f0b6"}.wi-owm-day-731:before{content:"\f063"}.wi-owm-day-741:before{content:"\f003"}.wi-owm-day-761:before{content:"\f063"}.wi-owm-day-762:before{content:"\f063"}.wi-owm-day-781:before{content:"\f056"}.wi-owm-day-800:before{content:"\f00d"}.wi-owm-day-801:before{content:"\f002"}.wi-owm-day-802:before{content:"\f002"}.wi-owm-day-803:before{content:"\f013"}.wi-owm-day-804:before{content:"\f013"}.wi-owm-day-900:before{content:"\f056"}.wi-owm-day-902:before{content:"\f073"}.wi-owm-day-903:before{content:"\f076"}.wi-owm-day-904:before{content:"\f072"}.wi-owm-day-906:before{content:"\f004"}.wi-owm-day-957:before{content:"\f050"}.wi-owm-night-200:before{content:"\f02d"}.wi-owm-night-201:before{content:"\f02d"}.wi-owm-night-202:before{content:"\f02d"}.wi-owm-night-210:before{content:"\f025"}.wi-owm-night-211:before{content:"\f025"}.wi-owm-night-212:before{content:"\f025"}.wi-owm-night-221:before{content:"\f025"}.wi-owm-night-230:before{content:"\f02d"}.wi-owm-night-231:before{content:"\f02d"}.wi-owm-night-232:before{content:"\f02d"}.wi-owm-night-300:before{content:"\f02b"}.wi-owm-night-301:before{content:"\f02b"}.wi-owm-night-302:before{content:"\f028"}.wi-owm-night-310:before{content:"\f028"}.wi-owm-night-311:before{content:"\f028"}.wi-owm-night-312:before{content:"\f028"}.wi-owm-night-313:before{content:"\f028"}.wi-owm-night-314:before{content:"\f028"}.wi-owm-night-321:before{content:"\f02b"}.wi-owm-night-500:before{content:"\f02b"}.wi-owm-night-501:before{content:"\f028"}.wi-owm-night-502:before{content:"\f028"}.wi-owm-night-503:before{content:"\f028"}.wi-owm-night-504:before{content:"\f028"}.wi-owm-night-511:before{content:"\f026"}.wi-owm-night-520:before{content:"\f029"}.wi-owm-night-521:before{content:"\f029"}.wi-owm-night-522:before{content:"\f029"}.wi-owm-night-531:before{content:"\f02c"}.wi-owm-night-600:before{content:"\f02a"}.wi-owm-night-601:before{content:"\f0b4"}.wi-owm-night-602:before{content:"\f02a"}.wi-owm-night-611:before{content:"\f026"}.wi-owm-night-612:before{content:"\f026"}.wi-owm-night-615:before{content:"\f026"}.wi-owm-night-616:before{content:"\f026"}.wi-owm-night-620:before{content:"\f026"}.wi-owm-night-621:before{content:"\f02a"}.wi-owm-night-622:before{content:"\f02a"}.wi-owm-night-701:before{content:"\f04a"}.wi-owm-night-711:before{content:"\f062"}.wi-owm-night-721:before{content:"\f0b6"}.wi-owm-night-731:before{content:"\f063"}.wi-owm-night-741:before{content:"\f04a"}.wi-owm-night-761:before{content:"\f063"}.wi-owm-night-762:before{content:"\f063"}.wi-owm-night-781:before{content:"\f056"}.wi-owm-night-800:before{content:"\f02e"}.wi-owm-night-801:before{content:"\f081"}.wi-owm-night-802:before{content:"\f086"}.wi-owm-night-803:before{content:"\f013"}.wi-owm-night-804:before{content:"\f013"}.wi-owm-night-900:before{content:"\f056"}.wi-owm-night-902:before{content:"\f073"}.wi-owm-night-903:before{content:"\f076"}.wi-owm-night-904:before{content:"\f072"}.wi-owm-night-906:before{content:"\f024"}.wi-owm-night-957:before{content:"\f050"}.wi-wu-chanceflurries:before{content:"\f064"}.wi-wu-chancerain:before{content:"\f019"}.wi-wu-chancesleat:before{content:"\f0b5"}.wi-wu-chancesnow:before{content:"\f01b"}.wi-wu-chancetstorms:before{content:"\f01e"}.wi-wu-clear:before{content:"\f00d"}.wi-wu-cloudy:before{content:"\f002"}.wi-wu-flurries:before{content:"\f064"}.wi-wu-hazy:before{content:"\f0b6"}.wi-wu-mostlycloudy:before{content:"\f002"}.wi-wu-mostlysunny:before{content:"\f00d"}.wi-wu-partlycloudy:before{content:"\f002"}.wi-wu-partlysunny:before{content:"\f00d"}.wi-wu-rain:before{content:"\f01a"}.wi-wu-sleat:before{content:"\f0b5"}.wi-wu-snow:before{content:"\f01b"}.wi-wu-sunny:before{content:"\f00d"}.wi-wu-tstorms:before{content:"\f01e"}.wi-wu-unknown:before{content:"\f00d"}/*# sourceMappingURL=weather-icons.min.css.map */
# '''


