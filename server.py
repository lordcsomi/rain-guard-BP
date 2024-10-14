from flask import Flask, jsonify, redirect
from bs4 import BeautifulSoup
import requests


# config
REPLACE = True
PORT = 5000
HOST = '0.0.0.0'
URL = "https://www.idokep.hu/elorejelzes/budapest"
API = "/weather"


app = Flask("weather")
weather_data_list = []

replace_dict = {
    "Á": "A",
    "á": "a",
    "É": "E",
    "é": "e",
    "Í": "I",
    "í": "i",
    "Ó": "O",
    "ó": "o",
    "Ö": "O",
    "ö": "o",
    "Ő": "O",
    "ő": "o",
    "Ú": "U",
    "ú": "u",
    "Ü": "U",
    "ü": "u",
    "Ű": "U",
    "ű": "u"
}

@app.route(API, methods=['GET'])
def get_weather():
    response = requests.get(URL)
    if response.status_code != 200:
        return jsonify({"error": "Weather data not available"}), 500

    soup = BeautifulSoup(response.content, 'html.parser')
    if soup is None:
        return jsonify({"error": "Weather data not available"}), 500

    forecast_elements = soup.find_all("div", class_="ik new-hourly-forecast-card")
    if forecast_elements is None:
        return jsonify({"error": "Weather data not available"}), 500

    weather_data_list = []
    for forecast_element in forecast_elements:
        hour = forecast_element.find("div", class_="ik new-hourly-forecast-hour").text.strip()
        cloudiness = forecast_element.find("div", class_="ik forecast-icon-container").a["data-bs-content"]
        temp_text = forecast_element.find("div", class_="ik tempBarGraph").div.a["data-bs-content"]
        temp_value = forecast_element.find("div", class_="ik tempBarGraph").div.a.text.strip()
        wind = forecast_element.find("div", class_="ik hourly-wind").a["data-bs-content"]
        rain_chance_value = forecast_element.find("div", class_="ik hourly-rain-chance").a.text.strip().split("%")[0] if forecast_element.find("div", class_="ik hourly-rain-chance") else None

        # replace Hungarian characters with English ones
        if REPLACE:
            for hungarian, english in replace_dict.items():
                cloudiness = cloudiness.replace(hungarian, english)
                wind = wind.replace(hungarian, english)

        hourly_data = {
            "hour": hour,
            "cloudiness": cloudiness,
            "temperature": temp_value,
            "wind": wind,
            "rain_chance": rain_chance_value
        }
        weather_data_list.append(hourly_data)

    return jsonify(weather_data_list)

@app.errorhandler(404)
def page_not_found(error):
    return redirect('/weather')

if __name__ == '__main__':
    print(f"Server IP: {HOST}, Port: {PORT}")
    print(f"Access /weather to get weather data")
    app.run(host=HOST, port=PORT)
