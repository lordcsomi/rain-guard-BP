import requests
from bs4 import BeautifulSoup
import logging
import datetime


logging.basicConfig(filename='weather.log', level=logging.INFO, format='%(asctime)s - %(message)s', encoding='utf-8')
starting_time = datetime.datetime.now()
logging.info(f"Starting the weather forecast script at {starting_time}")

URL = "https://www.idokep.hu/elorejelzes/budapest"
CHECKED_HOURS = ["6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"]
RAIN_TRIGGER = 10
weather_data = {}

response = requests.get(URL)
if response.status_code != 200:
    logging.error(f"Error while downloading the website. Status code: {response.status_code}")
    exit(1)
soup = BeautifulSoup(response.content, 'html.parser')
if soup is None:
    logging.error("Error while parsing the website. Soup is None")
    exit(1)
forecast_elements = soup.find_all("div", class_="ik new-hourly-forecast-card")
if forecast_elements is None:
    logging.error("Error while parsing the website. Forecast elements are None")
    exit(1)

checked_hours = []
for forecast_element in forecast_elements:
    hour = forecast_element.find("div", class_="ik new-hourly-forecast-hour").text.strip()
    if hour in checked_hours:
        break
    cloudiness = forecast_element.find("div", class_="ik forecast-icon-container").a["data-bs-content"]
    temp_text = forecast_element.find("div", class_="ik tempBarGraph").div.a["data-bs-content"]
    temp_value = forecast_element.find("div", class_="ik tempBarGraph").div.a.text.strip()
    wind = forecast_element.find("div", class_="ik hourly-wind").a["data-bs-content"]
    rain_chance_value = forecast_element.find("div", class_="ik hourly-rain-chance").a.text.strip().split("%")[0] if forecast_element.find("div", class_="ik hourly-rain-chance") else None
    weather_data[hour] = {"cloudiness": cloudiness, "temperature": temp_value, "wind": wind, "rain_chance": rain_chance_value}
    checked_hours.append(hour)
    
for hour in CHECKED_HOURS:
    if weather_data[hour]["rain_chance"] is not None and int(weather_data[hour]["rain_chance"]) > RAIN_TRIGGER:
        logging.info(f"Rain is expected at {hour} o'clock. {weather_data[hour]}")
        
ending_time = datetime.datetime.now()
logging.info(f"Finished the weather forecast script at {ending_time}")
logging.info(f"Script ran for {(ending_time - starting_time).total_seconds()} seconds")