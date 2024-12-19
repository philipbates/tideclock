import requests
from datetime import datetime, timedelta

import matplotlib.pyplot as plt

# OpenWeather API key
API_KEY = 'your_api_key_here'

# Coordinates for Grange, IE
LAT = 54.4044
LON = -8.5602

# URL for OpenWeather API
url = f'http://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric'

# Fetch weather data
response = requests.get(url)
data = response.json()

# Extract relevant data
timestamps = []
rainfall = []

for entry in data['list']:
    timestamp = datetime.utcfromtimestamp(entry['dt'])
    if timestamp <= datetime.utcnow() + timedelta(hours=12):
        timestamps.append(timestamp)
        rain = entry.get('rain', {}).get('3h', 0)
        rainfall.append(rain)

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(timestamps, rainfall, marker='o')
plt.title('Predicted Rainfall for the Next 12 Hours in Grange, IE')
plt.xlabel('Time')
plt.ylabel('Rainfall (mm)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()