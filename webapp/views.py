from django.shortcuts import render
import requests
import geocoder
from timezonefinder import timezonefinder
import json
import os
from django.conf import settings
# Create your views here.
def home(request):
    apiKey = 'q9iopHj6fBtlpBflx9ewLcK1arBp6Tvo'
    g = geocoder.ip('me')
    lat = g.latlng[0]
    lon = g.latlng[1]
    city = g.city

    APIurl = f'https://api.tomorrow.io/v4/timelines?location={lat},{lon}&fields=temperature,humidity,weatherCode&timesteps=30m&units=imperial&apikey={apiKey}'
    
    response = requests.get(APIurl)
    if response.status_code == 200:
        weather_data = response.json()
        weatherCode = weather_data['data']['timelines'][0]['intervals'][0]['values']['weatherCode']
        my_static_file = os.path.join(settings.STATIC_ROOT, 'weather_codes.json')
        with open(my_static_file) as f:
            weather_code_list = json.load(f)
        weatherIcon = weather_code_list[str(weatherCode)]+".svg"

        time_place =  timezonefinder.TimezoneFinder().timezone_at(lng=lon, lat=lat)
        my_static_file = os.path.join(settings.STATIC_ROOT, 'time_zones.json')
        with open(my_static_file) as f:
            timezone_offset = json.load(f)
        timeVar = int(weather_data['data']['timelines'][0]['intervals'][0]['startTime'].split('T')[1].split(':')[0]) + int(timezone_offset[time_place].split(':')[0])
        print(timeVar)
        if (int(timeVar) > 18 and int(timeVar) < 24) or (int(timeVar) > 0 and int(timeVar) < 6):
            if weatherIcon == "clear_day.svg":
                weatherIcon = "clear_night.svg"
            if weatherIcon == "mostly_clear_day.svg":
                weatherIcon = "mostly_clear_night.svg"
            if weatherIcon == "partly_cloudy_day.svg":
                weatherIcon = "partly_cloudy_night.svg"
            
        homeview_data = {
            'city': city,
            'temperature': weather_data['data']['timelines'][0]['intervals'][0]['values']['temperature'],
            'humidity': weather_data['data']['timelines'][0]['intervals'][0]['values']['humidity'],
            'weatherIcon': weatherIcon, 
        }

        return render(request, 'index.html', {'homeview_data': homeview_data})

    else:
        print(response.status_code)
        return render(request, 'index.html')
    
        

