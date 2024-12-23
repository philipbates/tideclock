import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt



def fetch_met_eireann_data(from_date, to_date):
    print("Fetching data from Met Éireann...")
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

def new_parse_data(xml_string):
    # Parse the XML data
    root = ET.fromstring(xml_string)
    output_dict = {}

    # Find and extract the relevant data
    for time in root.findall(".//time"):
        precipitation = time.find(".//precipitation")
        symbol = time.find(".//symbol")

        if precipitation is not None and symbol is not None:
            probability = precipitation.get("probability")
            symbol_id = symbol.get("id")
            time_from = time.get("from")
            font_symbol = map_met_to_font(symbol_id)
            unicode_symbol = map_symbol_to_unicode(font_symbol)
            output_dict[time_from] = {
                'symbol': symbol_id,
                'unicode': unicode_symbol,
                'precipitation_probability': probability
            }
            print(f"time: {time_from} Symbol ID: {symbol_id}, Precipitation Probability: {probability}%")
    return output_dict
# Function to parse XML and extract specific values
# def extract_weather_data(xml_string, start_time, end_time, elements_to_extract):
#     # Parse the XML string
#     root = ET.fromstring(xml_string)
#     weather_data = {}
    
#     # Navigate to the product section where forecast data is stored
#     product = root.find('product')
    
#     # Iterate through each time element and extract data
#     for time_element in product.findall('time'):
#         from_time = time_element.get('from')
#         to_time = time_element.get('to')
#         location = time_element.find('location')
#         precipitation = location.find('precipitation')
#         print('precipitation:', precipitation)
            
#         # Only proceed if there is precipitation data
#         if precipitation is not None:
#             data_extracted = {}
            
#             # Check for each requested element and gather data
#             for element in elements_to_extract:
#                 if element == 'symbol':
#                     symbol = location.find('symbol')
#                     if symbol is not None:
#                         data_extracted['symbol'] = symbol.get('id')
#                 if element == 'precipitation':
#                     data_extracted['precipitation_mm'] = precipitation.get('value')
#                     # data_extracted['precipitation_probability'] = precipitation.get('probability')
            
#             # Print the extracted data
#             print(f"Data from {from_time} to {to_time}: {data_extracted}")
#             weather_data[from_time] = data_extracted

#             return weather_data

# Function to convert weather data to output dictionary

# Define the mapping of weather symbols to font icons



    # Path to the XML file
    
def map_met_to_font(symbol):
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
        "HeavySnow": "wi-snow"}
    return symbol_to_icon[symbol]
def map_symbol_to_unicode(symbol):
    symbol_map = {
        "wi_day_sunny":"&#xf00d",
        "wi_day_cloudy":"&#xf002",
        "wi_day_cloudy_gusts":"&#xf000",
        "wi_day_cloudy_windy":"&#xf001",
        "wi_day_fog":"&#xf003",
        "wi_day_hail":"&#xf004",
        "wi_day_haze":"&#xf0b6",
        "wi_day_lightning":"&#xf005",
        "wi_day_rain":"&#xf008",
        "wi_day_rain_mix":"&#xf006",
        "wi_day_rain_wind":"&#xf007",
        "wi_day_showers":"&#xf009",
        "wi_day_sleet":"&#xf0b2",
        "wi_day_sleet_storm":"&#xf068",
        "wi_day_snow":"&#xf00a",
        "wi_day_snow_thunderstorm":"&#xf06b",
        "wi_day_snow_wind":"&#xf065",
        "wi_day_sprinkle":"&#xf00b",
        "wi_day_storm_showers":"&#xf00e",
        "wi_day_sunny_overcast":"&#xf00c",
        "wi_day_thunderstorm":"&#xf010",
        "wi_day_windy":"&#xf085",
        "wi_solar_eclipse":"&#xf06e",
        "wi_hot":"&#xf072",
        "wi_day_cloudy_high":"&#xf07d",
        "wi_day_light_wind":"&#xf0c4",
        "wi_night_clear":"&#xf02e",
        "wi_night_alt_cloudy":"&#xf086",
        "wi_night_alt_cloudy_gusts":"&#xf022",
        "wi_night_alt_cloudy_windy":"&#xf023",
        "wi_night_alt_hail":"&#xf024",
        "wi_night_alt_lightning":"&#xf025",
        "wi_night_alt_rain":"&#xf028",
        "wi_night_alt_rain_mix":"&#xf026",
        "wi_night_alt_rain_wind":"&#xf027",
        "wi_night_alt_showers":"&#xf029",
        "wi_night_alt_sleet":"&#xf0b4",
        "wi_night_alt_sleet_storm":"&#xf06a",
        "wi_night_alt_snow":"&#xf02a",
        "wi_night_alt_snow_thunderstorm":"&#xf06d",
        "wi_night_alt_snow_wind":"&#xf067",
        "wi_night_alt_sprinkle":"&#xf02b",
        "wi_night_alt_storm_showers":"&#xf02c",
        "wi_night_alt_thunderstorm":"&#xf02d",
        "wi_night_cloudy":"&#xf031",
        "wi_night_cloudy_gusts":"&#xf02f",
        "wi_night_cloudy_windy":"&#xf030",
        "wi_night_fog":"&#xf04a",
        "wi_night_hail":"&#xf032",
        "wi_night_lightning":"&#xf033",
        "wi_night_partly_cloudy":"&#xf083",
        "wi_night_rain":"&#xf036",
        "wi_night_rain_mix":"&#xf034",
        "wi_night_rain_wind":"&#xf035",
        "wi_night_showers":"&#xf037",
        "wi_night_sleet":"&#xf0b3",
        "wi_night_sleet_storm":"&#xf069",
        "wi_night_snow":"&#xf038",
        "wi_night_snow_thunderstorm":"&#xf06c",
        "wi_night_snow_wind":"&#xf066",
        "wi_night_sprinkle":"&#xf039",
        "wi_night_storm_showers":"&#xf03a",
        "wi_night_thunderstorm":"&#xf03b",
        "wi_lunar_eclipse":"&#xf070",
        "wi_stars":"&#xf077",
        "wi_storm_showers":"&#xf01d",
        "wi_thunderstorm":"&#xf01e",
        "wi_night_alt_cloudy_high":"&#xf07e",
        "wi_night_cloudy_high":"&#xf080",
        "wi_night_alt_partly_cloudy":"&#xf081",
        "wi_cloud":"&#xf041",
        "wi_cloudy":"&#xf013",
        "wi_cloudy_gusts":"&#xf011",
        "wi_cloudy_windy":"&#xf012",
        "wi_fog":"&#xf014",
        "wi_hail":"&#xf015",
        "wi_rain":"&#xf019",
        "wi_rain_mix":"&#xf017",
        "wi_rain_wind":"&#xf018",
        "wi_showers":"&#xf01a",
        "wi_sleet":"&#xf0b5",
        "wi_snow":"&#xf01b",
        "wi_sprinkle":"&#xf01c",
        "wi_snow_wind":"&#xf064",
        "wi_smog":"&#xf074",
        "wi_smoke":"&#xf062",
        "wi_lightning":"&#xf016",
        "wi_raindrops":"&#xf04e",
        "wi_raindrop":"&#xf078",
        "wi_dust":"&#xf063",
        "wi_snowflake_cold":"&#xf076",
        "wi_windy":"&#xf021",
        "wi_strong_wind":"&#xf050",
        "wi_sandstorm":"&#xf082",
        "wi_earthquake":"&#xf0c6",
        "wi_fire":"&#xf0c7",
        "wi_flood":"&#xf07c",
        "wi_meteor":"&#xf071",
        "wi_tsunami":"&#xf0c5",
        "wi_volcano":"&#xf0c8",
        "wi_hurricane":"&#xf073",
        "wi_tornado":"&#xf056",
        "wi_small_craft_advisory":"&#xf0cc",
        "wi_gale_warning":"&#xf0cd",
        "wi_storm_warning":"&#xf0ce",
        "wi_hurricane_warning":"&#xf0cf",
        "wi_wind_direction":"&#xf0b1",
        "wi_alien":"&#xf075",
        "wi_celsius":"&#xf03c",
        "wi_fahrenheit":"&#xf045",
        "wi_degrees":"&#xf042",
        "wi_thermometer":"&#xf055",
        "wi_thermometer_exterior":"&#xf053",
        "wi_thermometer_internal":"&#xf054",
        "wi_cloud_down":"&#xf03d",
        "wi_cloud_up":"&#xf040",
        "wi_cloud_refresh":"&#xf03e",
        "wi_horizon":"&#xf047",
        "wi_horizon_alt":"&#xf046",
        "wi_sunrise":"&#xf051",
        "wi_sunset":"&#xf052",
        "wi_moonrise":"&#xf0c9",
        "wi_moonset":"&#xf0ca",
        "wi_refresh":"&#xf04c",
        "wi_refresh_alt":"&#xf04b",
        "wi_umbrella":"&#xf084",
        "wi_barometer":"&#xf079",
        "wi_humidity":"&#xf07a",
        "wi_na":"&#xf07b",
        "wi_train":"&#xf0cb",
        "wi_moon_new":"&#xf095",
        "wi_moon_waxing_crescent_1":"&#xf096",
        "wi_moon_waxing_crescent_2":"&#xf097",
        "wi_moon_waxing_crescent_3":"&#xf098",
        "wi_moon_waxing_crescent_4":"&#xf099",
        "wi_moon_waxing_crescent_5":"&#xf09a",
        "wi_moon_waxing_crescent_6":"&#xf09b",
        "wi_moon_first_quarter":"&#xf09c",
        "wi_moon_waxing_gibbous_1":"&#xf09d",
        "wi_moon_waxing_gibbous_2":"&#xf09e",
        "wi_moon_waxing_gibbous_3":"&#xf09f",
        "wi_moon_waxing_gibbous_4":"&#xf0a0",
        "wi_moon_waxing_gibbous_5":"&#xf0a1",
        "wi_moon_waxing_gibbous_6":"&#xf0a2",
        "wi_moon_full":"&#xf0a3",
        "wi_moon_waning_gibbous_1":"&#xf0a4",
        "wi_moon_waning_gibbous_2":"&#xf0a5",
        "wi_moon_waning_gibbous_3":"&#xf0a6",
        "wi_moon_waning_gibbous_4":"&#xf0a7",
        "wi_moon_waning_gibbous_5":"&#xf0a8",
        "wi_moon_waning_gibbous_6":"&#xf0a9",
        "wi_moon_third_quarter":"&#xf0aa",
        "wi_moon_waning_crescent_1":"&#xf0ab",
        "wi_moon_waning_crescent_2":"&#xf0ac",
        "wi_moon_waning_crescent_3":"&#xf0ad",
        "wi_moon_waning_crescent_4":"&#xf0ae",
        "wi_moon_waning_crescent_5":"&#xf0af",
        "wi_moon_waning_crescent_6":"&#xf0b0",
        "wi_moon_alt_new":"&#xf0eb",
        "wi_moon_alt_waxing_crescent_1":"&#xf0d0",
        "wi_moon_alt_waxing_crescent_2":"&#xf0d1",
        "wi_moon_alt_waxing_crescent_3":"&#xf0d2",
        "wi_moon_alt_waxing_crescent_4":"&#xf0d3",
        "wi_moon_alt_waxing_crescent_5":"&#xf0d4",
        "wi_moon_alt_waxing_crescent_6":"&#xf0d5",
        "wi_moon_alt_first_quarter":"&#xf0d6",
        "wi_moon_alt_waxing_gibbous_1":"&#xf0d7",
        "wi_moon_alt_waxing_gibbous_2":"&#xf0d8",
        "wi_moon_alt_waxing_gibbous_3":"&#xf0d9",
        "wi_moon_alt_waxing_gibbous_4":"&#xf0da",
        "wi_moon_alt_waxing_gibbous_5":"&#xf0db",
        "wi_moon_alt_waxing_gibbous_6":"&#xf0dc",
        "wi_moon_alt_full":"&#xf0dd",
        "wi_moon_alt_waning_gibbous_1":"&#xf0de",
        "wi_moon_alt_waning_gibbous_2":"&#xf0df",
        "wi_moon_alt_waning_gibbous_3":"&#xf0e0",
        "wi_moon_alt_waning_gibbous_4":"&#xf0e1",
        "wi_moon_alt_waning_gibbous_5":"&#xf0e2",
        "wi_moon_alt_waning_gibbous_6":"&#xf0e3",
        "wi_moon_alt_third_quarter":"&#xf0e4",
        "wi_moon_alt_waning_crescent_1":"&#xf0e5",
        "wi_moon_alt_waning_crescent_2":"&#xf0e6",
        "wi_moon_alt_waning_crescent_3":"&#xf0e7",
        "wi_moon_alt_waning_crescent_4":"&#xf0e8",
        "wi_moon_alt_waning_crescent_5":"&#xf0e9",
        "wi_moon_alt_waning_crescent_6":"&#xf0ea",
        "wi_moon_0":"&#xf095",
        "wi_moon_1":"&#xf096",
        "wi_moon_2":"&#xf097",
        "wi_moon_3":"&#xf098",
        "wi_moon_4":"&#xf099",
        "wi_moon_5":"&#xf09a",
        "wi_moon_6":"&#xf09b",
        "wi_moon_7":"&#xf09c",
        "wi_moon_8":"&#xf09d",
        "wi_moon_9":"&#xf09e",
        "wi_moon_10":"&#xf09f",
        "wi_moon_11":"&#xf0a0",
        "wi_moon_12":"&#xf0a1",
        "wi_moon_13":"&#xf0a2",
        "wi_moon_14":"&#xf0a3",
        "wi_moon_15":"&#xf0a4",
        "wi_moon_16":"&#xf0a5",
        "wi_moon_17":"&#xf0a6",
        "wi_moon_18":"&#xf0a7",
        "wi_moon_19":"&#xf0a8",
        "wi_moon_20":"&#xf0a9",
        "wi_moon_21":"&#xf0aa",
        "wi_moon_22":"&#xf0ab",
        "wi_moon_23":"&#xf0ac",
        "wi_moon_24":"&#xf0ad",
        "wi_moon_25":"&#xf0ae",
        "wi_moon_26":"&#xf0af",
        "wi_moon_27":"&#xf0b0",
        "wi_time_1":"&#xf08a",
        "wi_time_2":"&#xf08b",
        "wi_time_3":"&#xf08c",
        "wi_time_4":"&#xf08d",
        "wi_time_5":"&#xf08e",
        "wi_time_6":"&#xf08f",
        "wi_time_7":"&#xf090",
        "wi_time_8":"&#xf091",
        "wi_time_9":"&#xf092",
        "wi_time_10":"&#xf093",
        "wi_time_11":"&#xf094",
        "wi_time_12":"&#xf089",
        "wi_direction_up":"&#xf058",
        "wi_direction_up_right":"&#xf057",
        "wi_direction_right":"&#xf04d",
        "wi_direction_down_right":"&#xf088",
        "wi_direction_down":"&#xf044",
        "wi_direction_down_left":"&#xf043",
        "wi_direction_left":"&#xf048",
        "wi_direction_up_left":"&#xf087",
        "wi_wind_beaufort_0":"&#xf0b7",
        "wi_wind_beaufort_1":"&#xf0b8",
        "wi_wind_beaufort_2":"&#xf0b9",
        "wi_wind_beaufort_3":"&#xf0ba",
        "wi_wind_beaufort_4":"&#xf0bb",
        "wi_wind_beaufort_5":"&#xf0bc",
        "wi_wind_beaufort_6":"&#xf0bd",
        "wi_wind_beaufort_7":"&#xf0be",
        "wi_wind_beaufort_8":"&#xf0bf",
        "wi_wind_beaufort_9":"&#xf0c0",
        "wi_wind_beaufort_10":"&#xf0c1",
        "wi_wind_beaufort_11":"&#xf0c2",
        "wi_wind_beaufort_12":"&#xf0c3",
        "wi_yahoo_0":"&#xf056",
        "wi_yahoo_1":"&#xf00e",
        "wi_yahoo_2":"&#xf073",
        "wi_yahoo_3":"&#xf01e",
        "wi_yahoo_4":"&#xf01e",
        "wi_yahoo_5":"&#xf017",
        "wi_yahoo_6":"&#xf017",
        "wi_yahoo_7":"&#xf017",
        "wi_yahoo_8":"&#xf015",
        "wi_yahoo_9":"&#xf01a",
        "wi_yahoo_10":"&#xf015",
        "wi_yahoo_11":"&#xf01a",
        "wi_yahoo_12":"&#xf01a",
        "wi_yahoo_13":"&#xf01b",
        "wi_yahoo_14":"&#xf00a",
        "wi_yahoo_15":"&#xf064",
        "wi_yahoo_16":"&#xf01b",
        "wi_yahoo_17":"&#xf015",
        "wi_yahoo_18":"&#xf017",
        "wi_yahoo_19":"&#xf063",
        "wi_yahoo_20":"&#xf014",
        "wi_yahoo_21":"&#xf021",
        "wi_yahoo_22":"&#xf062",
        "wi_yahoo_23":"&#xf050",
        "wi_yahoo_24":"&#xf050",
        "wi_yahoo_25":"&#xf076",
        "wi_yahoo_26":"&#xf013",
        "wi_yahoo_27":"&#xf031",
        "wi_yahoo_28":"&#xf002",
        "wi_yahoo_29":"&#xf031",
        "wi_yahoo_30":"&#xf002",
        "wi_yahoo_31":"&#xf02e",
        "wi_yahoo_32":"&#xf00d",
        "wi_yahoo_33":"&#xf083",
        "wi_yahoo_34":"&#xf00c",
        "wi_yahoo_35":"&#xf017",
        "wi_yahoo_36":"&#xf072",
        "wi_yahoo_37":"&#xf00e",
        "wi_yahoo_38":"&#xf00e",
        "wi_yahoo_39":"&#xf00e",
        "wi_yahoo_40":"&#xf01a",
        "wi_yahoo_41":"&#xf064",
        "wi_yahoo_42":"&#xf01b",
        "wi_yahoo_43":"&#xf064",
        "wi_yahoo_44":"&#xf00c",
        "wi_yahoo_45":"&#xf00e",
        "wi_yahoo_46":"&#xf01b",
        "wi_yahoo_47":"&#xf00e",
        "wi_yahoo_3200":"&#xf077",
        "wi_forecast_io_clear_day":"&#xf00d",
        "wi_forecast_io_clear_night":"&#xf02e",
        "wi_forecast_io_rain":"&#xf019",
        "wi_forecast_io_snow":"&#xf01b",
        "wi_forecast_io_sleet":"&#xf0b5",
        "wi_forecast_io_wind":"&#xf050",
        "wi_forecast_io_fog":"&#xf014",
        "wi_forecast_io_cloudy":"&#xf013",
        "wi_forecast_io_partly_cloudy_day":"&#xf002",
        "wi_forecast_io_partly_cloudy_night":"&#xf031",
        "wi_forecast_io_hail":"&#xf015",
        "wi_forecast_io_thunderstorm":"&#xf01e",
        "wi_forecast_io_tornado":"&#xf056",
        "wi_wmo4680_0":"&#xf055",
        "wi_wmo4680_00":"&#xf055",
        "wi_wmo4680_1":"&#xf013",
        "wi_wmo4680_01":"&#xf013",
        "wi_wmo4680_2":"&#xf055",
        "wi_wmo4680_02":"&#xf055",
        "wi_wmo4680_3":"&#xf013",
        "wi_wmo4680_03":"&#xf013",
        "wi_wmo4680_4":"&#xf014",
        "wi_wmo4680_04":"&#xf014",
        "wi_wmo4680_5":"&#xf014",
        "wi_wmo4680_05":"&#xf014",
        "wi_wmo4680_10":"&#xf014",
        "wi_wmo4680_11":"&#xf014",
        "wi_wmo4680_12":"&#xf016",
        "wi_wmo4680_18":"&#xf050",
        "wi_wmo4680_20":"&#xf014",
        "wi_wmo4680_21":"&#xf017",
        "wi_wmo4680_22":"&#xf017",
        "wi_wmo4680_23":"&#xf019",
        "wi_wmo4680_24":"&#xf01b",
        "wi_wmo4680_25":"&#xf015",
        "wi_wmo4680_26":"&#xf01e",
        "wi_wmo4680_27":"&#xf063",
        "wi_wmo4680_28":"&#xf063",
        "wi_wmo4680_29":"&#xf063",
        "wi_wmo4680_30":"&#xf014",
        "wi_wmo4680_31":"&#xf014",
        "wi_wmo4680_32":"&#xf014",
        "wi_wmo4680_33":"&#xf014",
        "wi_wmo4680_34":"&#xf014",
        "wi_wmo4680_35":"&#xf014",
        "wi_wmo4680_40":"&#xf017",
        "wi_wmo4680_41":"&#xf01c",
        "wi_wmo4680_42":"&#xf019",
        "wi_wmo4680_43":"&#xf01c",
        "wi_wmo4680_44":"&#xf019",
        "wi_wmo4680_45":"&#xf015",
        "wi_wmo4680_46":"&#xf015",
        "wi_wmo4680_47":"&#xf01b",
        "wi_wmo4680_48":"&#xf01b",
        "wi_wmo4680_50":"&#xf01c",
        "wi_wmo4680_51":"&#xf01c",
        "wi_wmo4680_52":"&#xf019",
        "wi_wmo4680_53":"&#xf019",
        "wi_wmo4680_54":"&#xf076",
        "wi_wmo4680_55":"&#xf076",
        "wi_wmo4680_56":"&#xf076",
        "wi_wmo4680_57":"&#xf01c",
        "wi_wmo4680_58":"&#xf019",
        "wi_wmo4680_60":"&#xf01c",
        "wi_wmo4680_61":"&#xf01c",
        "wi_wmo4680_62":"&#xf019",
        "wi_wmo4680_63":"&#xf019",
        "wi_wmo4680_64":"&#xf015",
        "wi_wmo4680_65":"&#xf015",
        "wi_wmo4680_66":"&#xf015",
        "wi_wmo4680_67":"&#xf017",
        "wi_wmo4680_68":"&#xf017",
        "wi_wmo4680_70":"&#xf01b",
        "wi_wmo4680_71":"&#xf01b",
        "wi_wmo4680_72":"&#xf01b",
        "wi_wmo4680_73":"&#xf01b",
        "wi_wmo4680_74":"&#xf076",
        "wi_wmo4680_75":"&#xf076",
        "wi_wmo4680_76":"&#xf076",
        "wi_wmo4680_77":"&#xf01b",
        "wi_wmo4680_78":"&#xf076",
        "wi_wmo4680_80":"&#xf019",
        "wi_wmo4680_81":"&#xf01c",
        "wi_wmo4680_82":"&#xf019",
        "wi_wmo4680_83":"&#xf019",
        "wi_wmo4680_84":"&#xf01d",
        "wi_wmo4680_85":"&#xf017",
        "wi_wmo4680_86":"&#xf017",
        "wi_wmo4680_87":"&#xf017",
        "wi_wmo4680_89":"&#xf015",
        "wi_wmo4680_90":"&#xf016",
        "wi_wmo4680_91":"&#xf01d",
        "wi_wmo4680_92":"&#xf01e",
        "wi_wmo4680_93":"&#xf01e",
        "wi_wmo4680_94":"&#xf016",
        "wi_wmo4680_95":"&#xf01e",
        "wi_wmo4680_96":"&#xf01e",
        "wi_wmo4680_99":"&#xf056",
        "wi_owm_200":"&#xf01e",
        "wi_owm_201":"&#xf01e",
        "wi_owm_202":"&#xf01e",
        "wi_owm_210":"&#xf016",
        "wi_owm_211":"&#xf016",
        "wi_owm_212":"&#xf016",
        "wi_owm_221":"&#xf016",
        "wi_owm_230":"&#xf01e",
        "wi_owm_231":"&#xf01e",
        "wi_owm_232":"&#xf01e",
        "wi_owm_300":"&#xf01c",
        "wi_owm_301":"&#xf01c",
        "wi_owm_302":"&#xf019",
        "wi_owm_310":"&#xf017",
        "wi_owm_311":"&#xf019",
        "wi_owm_312":"&#xf019",
        "wi_owm_313":"&#xf01a",
        "wi_owm_314":"&#xf019",
        "wi_owm_321":"&#xf01c",
        "wi_owm_500":"&#xf01c",
        "wi_owm_501":"&#xf019",
        "wi_owm_502":"&#xf019",
        "wi_owm_503":"&#xf019",
        "wi_owm_504":"&#xf019",
        "wi_owm_511":"&#xf017",
        "wi_owm_520":"&#xf01a",
        "wi_owm_521":"&#xf01a",
        "wi_owm_522":"&#xf01a",
        "wi_owm_531":"&#xf01d",
        "wi_owm_600":"&#xf01b",
        "wi_owm_601":"&#xf01b",
        "wi_owm_602":"&#xf0b5",
        "wi_owm_611":"&#xf017",
        "wi_owm_612":"&#xf017",
        "wi_owm_615":"&#xf017",
        "wi_owm_616":"&#xf017",
        "wi_owm_620":"&#xf017",
        "wi_owm_621":"&#xf01b",
        "wi_owm_622":"&#xf01b",
        "wi_owm_701":"&#xf01a",
        "wi_owm_711":"&#xf062",
        "wi_owm_721":"&#xf0b6",
        "wi_owm_731":"&#xf063",
        "wi_owm_741":"&#xf014",
        "wi_owm_761":"&#xf063",
        "wi_owm_762":"&#xf063",
        "wi_owm_771":"&#xf011",
        "wi_owm_781":"&#xf056",
        "wi_owm_800":"&#xf00d",
        "wi_owm_801":"&#xf011",
        "wi_owm_802":"&#xf011",
        "wi_owm_803":"&#xf012",
        "wi_owm_804":"&#xf013",
        "wi_owm_900":"&#xf056",
        "wi_owm_901":"&#xf01d",
        "wi_owm_902":"&#xf073",
        "wi_owm_903":"&#xf076",
        "wi_owm_904":"&#xf072",
        "wi_owm_905":"&#xf021",
        "wi_owm_906":"&#xf015",
        "wi_owm_957":"&#xf050",
        "wi_owm_day_200":"&#xf010",
        "wi_owm_day_201":"&#xf010",
        "wi_owm_day_202":"&#xf010",
        "wi_owm_day_210":"&#xf005",
        "wi_owm_day_211":"&#xf005",
        "wi_owm_day_212":"&#xf005",
        "wi_owm_day_221":"&#xf005",
        "wi_owm_day_230":"&#xf010",
        "wi_owm_day_231":"&#xf010",
        "wi_owm_day_232":"&#xf010",
        "wi_owm_day_300":"&#xf00b",
        "wi_owm_day_301":"&#xf00b",
        "wi_owm_day_302":"&#xf008",
        "wi_owm_day_310":"&#xf008",
        "wi_owm_day_311":"&#xf008",
        "wi_owm_day_312":"&#xf008",
        "wi_owm_day_313":"&#xf008",
        "wi_owm_day_314":"&#xf008",
        "wi_owm_day_321":"&#xf00b",
        "wi_owm_day_500":"&#xf00b",
        "wi_owm_day_501":"&#xf008",
        "wi_owm_day_502":"&#xf008",
        "wi_owm_day_503":"&#xf008",
        "wi_owm_day_504":"&#xf008",
        "wi_owm_day_511":"&#xf006",
        "wi_owm_day_520":"&#xf009",
        "wi_owm_day_521":"&#xf009",
        "wi_owm_day_522":"&#xf009",
        "wi_owm_day_531":"&#xf00e",
        "wi_owm_day_600":"&#xf00a",
        "wi_owm_day_601":"&#xf0b2",
        "wi_owm_day_602":"&#xf00a",
        "wi_owm_day_611":"&#xf006",
        "wi_owm_day_612":"&#xf006",
        "wi_owm_day_615":"&#xf006",
        "wi_owm_day_616":"&#xf006",
        "wi_owm_day_620":"&#xf006",
        "wi_owm_day_621":"&#xf00a",
        "wi_owm_day_622":"&#xf00a",
        "wi_owm_day_701":"&#xf009",
        "wi_owm_day_711":"&#xf062",
        "wi_owm_day_721":"&#xf0b6",
        "wi_owm_day_731":"&#xf063",
        "wi_owm_day_741":"&#xf003",
        "wi_owm_day_761":"&#xf063",
        "wi_owm_day_762":"&#xf063",
        "wi_owm_day_771":"&#xf000",
        "wi_owm_day_781":"&#xf056",
        "wi_owm_day_800":"&#xf00d",
        "wi_owm_day_801":"&#xf000",
        "wi_owm_day_802":"&#xf000",
        "wi_owm_day_803":"&#xf000",
        "wi_owm_day_804":"&#xf00c",
        "wi_owm_day_900":"&#xf056",
        "wi_owm_day_901":"&#xf00e",
        "wi_owm_day_902":"&#xf073",
        "wi_owm_day_903":"&#xf076",
        "wi_owm_day_904":"&#xf072",
        "wi_owm_day_905":"&#xf0c4",
        "wi_owm_day_906":"&#xf004",
        "wi_owm_day_957":"&#xf050",
        "wi_owm_night_200":"&#xf02d",
        "wi_owm_night_201":"&#xf02d",
        "wi_owm_night_202":"&#xf02d",
        "wi_owm_night_210":"&#xf025",
        "wi_owm_night_211":"&#xf025",
        "wi_owm_night_212":"&#xf025",
        "wi_owm_night_221":"&#xf025",
        "wi_owm_night_230":"&#xf02d",
        "wi_owm_night_231":"&#xf02d",
        "wi_owm_night_232":"&#xf02d",
        "wi_owm_night_300":"&#xf02b",
        "wi_owm_night_301":"&#xf02b",
        "wi_owm_night_302":"&#xf028",
        "wi_owm_night_310":"&#xf028",
        "wi_owm_night_311":"&#xf028",
        "wi_owm_night_312":"&#xf028",
        "wi_owm_night_313":"&#xf028",
        "wi_owm_night_314":"&#xf028",
        "wi_owm_night_321":"&#xf02b",
        "wi_owm_night_500":"&#xf02b",
        "wi_owm_night_501":"&#xf028",
        "wi_owm_night_502":"&#xf028",
        "wi_owm_night_503":"&#xf028",
        "wi_owm_night_504":"&#xf028",
        "wi_owm_night_511":"&#xf026",
        "wi_owm_night_520":"&#xf029",
        "wi_owm_night_521":"&#xf029",
        "wi_owm_night_522":"&#xf029",
        "wi_owm_night_531":"&#xf02c",
        "wi_owm_night_600":"&#xf02a",
        "wi_owm_night_601":"&#xf0b4",
        "wi_owm_night_602":"&#xf02a",
        "wi_owm_night_611":"&#xf026",
        "wi_owm_night_612":"&#xf026",
        "wi_owm_night_615":"&#xf026",
        "wi_owm_night_616":"&#xf026",
        "wi_owm_night_620":"&#xf026",
        "wi_owm_night_621":"&#xf02a",
        "wi_owm_night_622":"&#xf02a",
        "wi_owm_night_701":"&#xf029",
        "wi_owm_night_711":"&#xf062",
        "wi_owm_night_721":"&#xf0b6",
        "wi_owm_night_731":"&#xf063",
        "wi_owm_night_741":"&#xf04a",
        "wi_owm_night_761":"&#xf063",
        "wi_owm_night_762":"&#xf063",
        "wi_owm_night_771":"&#xf022",
        "wi_owm_night_781":"&#xf056",
        "wi_owm_night_800":"&#xf02e",
        "wi_owm_night_801":"&#xf022",
        "wi_owm_night_802":"&#xf022",
        "wi_owm_night_803":"&#xf022",
        "wi_owm_night_804":"&#xf086",
        "wi_owm_night_900":"&#xf056",
        "wi_owm_night_901":"&#xf03a",
        "wi_owm_night_902":"&#xf073",
        "wi_owm_night_903":"&#xf076",
        "wi_owm_night_904":"&#xf072",
        "wi_owm_night_905":"&#xf021",
        "wi_owm_night_906":"&#xf024",
        "wi_owm_night_957":"&#xf050",
        "wi_wu_chanceflurries":"&#xf064",
        "wi_wu_chancerain":"&#xf019",
        "wi_wu_chancesleat":"&#xf0b5",
        "wi_wu_chancesnow":"&#xf01b",
        "wi_wu_chancetstorms":"&#xf01e",
        "wi_wu_clear":"&#xf00d",
        "wi_wu_cloudy":"&#xf002",
        "wi_wu_flurries":"&#xf064",
        "wi_wu_hazy":"&#xf0b6",
        "wi_wu_mostlycloudy":"&#xf002",
        "wi_wu_mostlysunny":"&#xf00d",
        "wi_wu_partlycloudy":"&#xf002",
        "wi_wu_partlysunny":"&#xf00d",
        "wi_wu_rain":"&#xf01a",
        "wi_wu_sleat":"&#xf0b5",
        "wi_wu_snow":"&#xf01b",
        "wi_wu_sunny":"&#xf00d",
        "wi_wu_tstorms":"&#xf01e",
        "wi_wu_unknown":"&#xf00d"}
    # Get the Unicode value for the symbol
    unicode_value = symbol_map[symbol]
    return unicode_value


#%%

def fetch_parse_data():
    from_date = "2024-12-15T00:00"
    to_date = "2024-12-17T23:00"
    response = fetch_met_eireann_data(from_date, to_date)
    xml_data = response.content.decode('utf-8')
    output_dict = new_parse_data(xml_data)
    return output_dict


if __name__ == "__main__":
    from_date = "2024-12-15T00:00"
    to_date = "2024-12-17T23:00"
    response = fetch_met_eireann_data(from_date, to_date)
    xml_data = response.content.decode('utf-8')
    print(xml_data)

    # output_dict = new_parse_data(xml_data)



    # # Extract times and probabilities for plotting
    # times = list(output_dict.keys())
    # probabilities = [float(data['precipitation_probability']) if data['precipitation_probability'] is not None else 0 for data in output_dict.values()]

    # # Plot the data
    # plt.figure(figsize=(10, 5))
    # plt.plot(times, probabilities, 'bo')  # 'bo' means blue color, round points
    # plt.xlabel('Time')
    # plt.ylabel('Precipitation Probability (%)')
    # plt.title('Precipitation Probability Over Time')
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.show()

    # Read the weathericons.xml file
    tree = ET.parse(r'weather-icons-master\font\weathericons.xml')
    root = tree.getroot()

    def get_unicode_value(icon_name):
        unicode_value = None
        for icon_string in root.findall('string'):
            if icon_string.get('name') == icon_name:
                unicode_value = icon_string.text
                break
            
        if unicode_value == None:
            unicode_value = "&#xf075"

        return unicode_value

    # Find the Unicode value for "wi-day-cloudy"
    unicode_value = None
    for icon_string in root.findall('string'):
        if icon_string.get('name') == 'wi_day_cloudy':  # Ensure correct attribute name
            unicode_value = icon_string.text  # Access the text of the element
            break

    if unicode_value:
        print(f"The Unicode value for 'wi-day-cloudy' is: {unicode_value}")
    else:
        print("Unicode value for 'wi-day-cloudy' not found.")



