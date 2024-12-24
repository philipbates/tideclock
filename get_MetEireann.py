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
            icon = symbol_to_icon.get(symbol, 'wi-na')
            output_dict[time_from] = {
                'symbol': symbol_id,
                'icon': icon,
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

# Path to the XML file
xml_file_path = r"weather-icons-master\font\weathericons.xml"

# Parse the XML to create a mapping of names to Unicode values
tree = ET.parse(xml_file_path)
root = tree.getroot()

unicode_mapping = {}
for string in root.findall('string'):
    name = string.attrib.get('name')
    unicode_value = string.text
    unicode_mapping[name] = unicode_value

# Update the dictionary to include Unicode values
updated_symbol_to_icon = {}
for key, value in symbol_to_icon.items():
    unicode_value = unicode_mapping.get(value, None)  # Get Unicode value from mapping
    updated_symbol_to_icon[key] = {
        "original": value,
        "unicode": unicode_value
    }

# Print the updated dictionary
for key, value in updated_symbol_to_icon.items():
    print(f"{key}: {value}")

def map_symbol_to_unicode(symbol,updated_symbol_to_icon):
    # Get the Unicode value for the symbol
    unicode_value = updated_symbol_to_icon.get(symbol, {}).get('unicode', 'wi-na')
    return unicode_value
# def convert_weather_data_to_output_dict(weather_data, symbol_to_icon):
#     output_dict = {}
#     for time, info in weather_data.items():
#         symbol = info.get('symbol', 'unknown')
#         precipitation_mm = info.get('precipitation_mm', 'unknown')
#         precipitation_probability = info.get('precipitation_probability', 'unknown')
#         icon = symbol_to_icon.get(symbol, 'wi-na')
#         output_dict[time] = {
#             'symbol': symbol,
#             'icon': icon,
#             'precipitation_mm': precipitation_mm,
#             'precipitation_probability': precipitation_probability
#         }
#     return output_dict


# def fetch_and_process_weather_data():
#     from_date = "2024-12-15T00:00"
#     to_date = "2024-12-17T23:00"
#     response = fetch_met_eireann_data(from_date, to_date)
#     # Specify the time range and elements to extract
#     start_time = from_date
#     end_time = to_date
#     elements_to_extract = ['symbol', 'precipitation']
#     xml_data = response.content.decode('utf-8')
#     print(xml_data)

#     new_parse_data(xml_data)

#     # Call the function
#     weather_data = extract_weather_data(xml_data, start_time, end_time, elements_to_extract)
#     print(weather_data)
#     #print the number of items in the dictionary


#     # Convert the weather data to an output dictionary
#     output_dict = convert_weather_data_to_output_dict(weather_data, symbol_to_icon)
#     return output_dict

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

    output_dict = new_parse_data(xml_data)



    # Extract times and probabilities for plotting
    times = list(output_dict.keys())
    probabilities = [float(data['precipitation_probability']) if data['precipitation_probability'] is not None else 0 for data in output_dict.values()]

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(times, probabilities, 'bo')  # 'bo' means blue color, round points
    plt.xlabel('Time')
    plt.ylabel('Precipitation Probability (%)')
    plt.title('Precipitation Probability Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()