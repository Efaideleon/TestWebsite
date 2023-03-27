import requests

class TimeAPI:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.response = self.__get_timeapi_response()

    #public methods
    def get_current_hour(self):
        return self.response['hour']

    #private methods
    def __get_timeapi_response(self):
        APIurl = f'https://timeapi.io/api/Time/current/coordinate?latitude={self.lat}&longitude={self.lon}'
        response = requests.get(APIurl)
        if response.status_code == 200:
            return response.json()
        else:
            return None
