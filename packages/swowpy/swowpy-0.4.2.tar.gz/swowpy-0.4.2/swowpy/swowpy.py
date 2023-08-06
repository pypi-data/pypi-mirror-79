#Small wrapper for openweathermap
import requests
import json

class Swowpy:

    def __init__(self,api_key,city):

        self.key = api_key
        self.city = city

    def _create_url(self,city,measure):
        if measure == "weather":
            URL = "http://api.openweathermap.org/data/2.5/weather?q="
            URL += city
            URL += "&appid=" + self.key
            return URL

    def raw(self):
        URL = self._create_url(self.city,"weather")
        response = requests.get(url = URL)
        return response.json()

    def current_weather(self,*args):
        URL = self._create_url(self.city,"weather")
        response = requests.get(url = URL)
        if "Description" in args:
             return response.json()['weather'][0]['description'] 

        else:
            return response.json()['weather'][0]['main']    

    def temperature(self,**kwargs):
        URL = self._create_url(self.city,"weather")
        response = requests.get(url = URL)
        if kwargs.get('unit') == "Celsius":
             return float(response.json()['main']['temp'])-273.15
 
        else: 
             return response.json()['main']['temp']    

    
    def wind(self):
        URL = self._create_url(self.city,"weather")
        response = requests.get(url = URL)
        return response.json()['wind']['speed'],response.json()['wind']['deg']    

    def humidity(self):
        URL = self._create_url(self.city,"weather")
        response = requests.get(url = URL)
        return response.json()['main']['humidity']    

    def pressure(self):
        URL = self._create_url(self.city,"weather")
        response = requests.get(url = URL)
        return response.json()['main']['pressure']    

        
