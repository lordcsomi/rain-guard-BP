from flask import Flask, jsonify, request, render_template
from bs4 import BeautifulSoup
import requests
import logging
import datetime
import sys
import psutil
import os

app = Flask("weather")

logging.basicConfig(filename='weather.log', level=logging.INFO, format='%(asctime)s - %(message)s', encoding='utf-8')
starting_time = datetime.datetime.now()
logging.info(f"Starting the weather forecast script at {starting_time}")

URL = "https://www.idokep.hu/elorejelzes/budapest"
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

@app.route('/weather', methods=['GET'])
def get_weather():
    response = requests.get(URL)
    if response.status_code != 200:
        logging.error(f"Error while downloading the website. Status code: {response.status_code}")
        return jsonify({"error": "Weather data not available"}), 500

    soup = BeautifulSoup(response.content, 'html.parser')
    if soup is None:
        logging.error("Error while parsing the website. Soup is None")
        return jsonify({"error": "Weather data not available"}), 500

    forecast_elements = soup.find_all("div", class_="ik new-hourly-forecast-card")
    if forecast_elements is None:
        logging.error("Error while parsing the website. Forecast elements are None")
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

@app.route('/log', methods=['GET'])
def get_log():
    try:
        with open('weather.log', 'r') as log_file:
            log_data = log_file.read()
        return log_data
    except FileNotFoundError:
        return "Log file not found."

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "password":
            return render_template('admin.html')
        else:
            return "Invalid credentials. Access Denied."
    return render_template('login.html')

@app.route('/admin/telemetry', methods=['GET'])
def get_system_performance():
    try:
        cpu_usage = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        system_info = {
            "CPU Usage": f"{cpu_usage}%",
            "RAM Usage": f"{ram}%",
            "Disk Usage": f"{disk}%"
        }
        return jsonify(system_info)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/clear-log', methods=['GET'])
def clear_log():
    try:
        open('weather.log', 'w').close()
        return "Log file cleared."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/restart-service', methods=['GET'])
def restart_service():
    # Code to restart the service goes here
    return "Service is restarting..."

@app.route('/admin/restart-pi', methods=['GET'])
def restart_pi():
    # Code to restart the Raspberry Pi goes here
    return "Raspberry Pi is restarting..."

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    print(f"Server IP: {host}, Port: {port}")
    print(f"Access /weather to get weather data")
    app.run(host=host, port=port)
