import geocoder
import requests
from utils.time_api import *
from utils.utility_functions import *
class WeatherAPI:
    def __init__(self, apikey, ip):
        self.apikey = apikey
        self.g = geocoder.ip(ip)
        self.lat = self.g.latlng[0]
        self.lon = self.g.latlng[1]
        self.city = self.g.city 
        self.weather_data = {}
        self.response = self.__get_tomorrowio_response()

    #public methods
    def get_all_weather_data(self):
        if self.response == None:
            return self.weather_data
        self.__add_city()
        self.__add_temperature()
        self.__add_humidity()
        self.__add_weatherIcon()
        return self.weather_data

    #private methods
    def __add_city(self):
        self.__add_weather_data('city', self.city)

    def __add_temperature(self):
        temperature = self.response['data']['timelines'][0]['intervals'][0]['values']['temperature']
        self.__add_weather_data('temperature', temperature)

    def __add_humidity(self):
        humidity = self.response['data']['timelines'][0]['intervals'][0]['values']['humidity']
        self.__add_weather_data('humidity', humidity)

    def __add_weatherIcon(self):
        Time_API = TimeAPI(self.lat, self.lon)
        weather_code_number = self.response['data']['timelines'][0]['intervals'][0]['values']['weatherCode']
        weather_code_list = read_json_file('weather_codes.json')
        weather_icon_name = weather_code_list[str(weather_code_number)]
        weather_icon_svg =  self.__get_icon_based_on_time(weather_icon_name) +".svg"
        self.__add_weather_data('weatherIcon', weather_icon_svg)

    def __add_weather_data(self, key, value):
        self.weather_data[key] = value

    def __get_tomorrowio_response(self):
        APIurl = f'https://api.tomorrow.io/v4/timelines?location={self.lat},{self.lon}&fields=temperature,humidity,weatherCode&timesteps=30m&units=imperial&apikey={self.apikey}'
        response = requests.get(APIurl)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def __get_icon_based_on_time(self, weather_icon_name):
        Time_API = TimeAPI(self.lat, self.lon)
        current_time = Time_API.get_current_hour()
        if (int(current_time) > 18 and int(current_time) < 24) or (int(current_time) > 0 and int(current_time) < 6):
            if weather_icon_name == "clear_day.svg":
                weather_icon_name = "clear_night.svg"
            if weather_icon_name == "mostly_clear_day.svg":
                weather_icon_name = "mostly_clear_night.svg"
            if weather_icon_name == "partly_cloudy_day.svg":
                weather_icon_name = "partly_cloudy_night.svg"
        return weather_icon_name


