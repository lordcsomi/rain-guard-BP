
# Weather Forecast Service

This Python Flask application serves as a weather forecast service for Budapest. It retrieves weather data by scraping information from the idokep.hu website and provides this data through a RESTful API. The service fetches details such as cloudiness, temperature, wind, and the probability of rain for specific hours of the day.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)

## Installation

To use this service, follow these steps:

1. Ensure you have Python 3.x installed on your system.

2. Clone or download this repository to your local machine.

3. Install the required libraries by running the following command:

    ```bash
    pip install Flask requests beautifulsoup4
    ```

4. Run the Flask application:

    ```bash
    python server.py
    ```

## Usage

When you run the Flask application, it will start a server at `http://localhost:5000` and provide the weather data through the defined API endpoints.

Access `http://localhost:5000/weather` to get the weather data in JSON format.

## API Endpoints

The `/weather` endpoint returns the weather forecast for Budapest in the following format:

```json
[
    {
        "cloudiness": "erosen felhos",
        "hour": "14:00",
        "rain_chance": null,
        "temperature": "23",
        "wind": "Elenk delnyugati szel"
    },
    {
        "cloudiness": "kozepesen felhos",
        "hour": "15:00",
        "rain_chance": null,
        "temperature": "23",
        "wind": "Mersekelt delnyugati szel"
    }
    // ... Additional hours
]
```

Each entry in the response represents the weather forecast for a specific hour. The data includes details such as cloudiness, temperature, wind, and the probability of rain.

## Customization

You can customize the behavior of the Flask application by modifying the following variables in the `server.py` file:

- **PORT**: Change the port on which the Flask application runs.
- **HOST**: Modify the host IP (default is `0.0.0.0` to make it accessible locally).
- **URL**: Update the URL if you want to scrape weather data from a different location or website.
- **API**: Change the endpoint where weather data is accessed.

Additionally, you can extend or modify the data scraping logic to include more details, such as humidity, air pressure, or visibility. The `replace_dict` can also be expanded or customized for additional Hungarian character replacements.

## Contributing

If you'd like to contribute to this Flask-based weather service, feel free to fork the repository and submit a pull request with your enhancements. Ensure adherence to best practices for code quality and documentation.

Make sure to test your changes and provide clear descriptions in your pull request.

---

**Server Information:**

- **IP**: 0.0.0.0
- **Port**: 5000

**Note**: Access `/weather` to retrieve weather data once the Flask application is running.