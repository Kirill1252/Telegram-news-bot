import requests
from config import token_weather


def get_weather(city):
    try:
        request_link = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={token_weather}&units=metric")
        data = request_link.json()
        city = data["name"]
        current_weather = data["main"]["temp"]
        air_humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_dict = {
            'city': city,
            'temperature': current_weather,
            'air_humidity': air_humidity,
            'wind_speed': wind_speed
        }

        return weather_dict

    except Exception as ex:
        return f'{ex}: Неверное название города'

