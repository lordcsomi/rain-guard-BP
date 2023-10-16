# Weather Forecast Script

 This Python script is designed to provide weather forecasts for Budapest by scraping data from the idokep.hu website. It retrieves information about cloudiness, temperature, wind, and the probability of rain for specific hours of the day. The script logs this data to a file and checks for the likelihood of rain in the next few hours based on user-defined criteria.

# Table of Contents

 - [Installation](#installation)
 - [Usage](#usage)
 - [Customization](#customization)
 - [Contributing](#contributing)

# Installation

 To use this script, follow these steps:

 1. Ensure you have Python 3.x installed on your system.

 2. Clone or download this repository to your local machine.

 3. Install the required libraries by running the following command:

    ```bash
    pip install requests beautifulsoup4
    ```

 4. Run the script:

    ```bash
    python weather_forecast.py
    ```

# Usage

 When you run the script, it will perform the following actions:

 1. Access the idokep.hu website to fetch the weather data for Budapest.

 2. Check for the likelihood of rain at specific hours during the day (as specified in the `CHECKED_HOURS` list).

 3. Log weather information, including cloudiness, temperature, wind speed, and rain probability to a file named `weather.log`.

 4. Identify and log hours when rain is expected based on the defined threshold (`RAIN_TRIGGER`).

 The script will display information about rain expectations and will indicate if no rain is expected in the next few hours.

# Customization

 You can customize the script by modifying the following variables:

 - `CHECKED_HOURS`: Change this list to specify the hours you want to check for rain. You can add or remove hours as needed.

 - `RAIN_TRIGGER`: Adjust this value to change the probability threshold for considering rain. If the rain chance at a specified hour is greater than or equal to this threshold, the script will log it.

# Contributing

 If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your enhancements. Please follow best practices for code quality and documentation.

