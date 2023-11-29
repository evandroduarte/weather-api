import requests
import os
from datetime import datetime
from utils.logger_startup import logger

OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")
WEATHER_API_URL = os.environ.get("WEATHER_API_URL")

if OPENWEATHERMAP_API_KEY is None or WEATHER_API_URL is None:
    raise EnvironmentError(
        "OPENWEATHERMAP_API_KEY or WEATHER_API_URL environment variables not configured."
    )


def get_city_data(city):
    """
    Get geographical data for a given city from the OpenWeatherMap API.

    Parameters:
    - city (str): The name of the city.

    Returns:
    dict: Geographical data including latitude, longitude, and city name.
    """
    try:
        response = requests.get(
            f"{WEATHER_API_URL}/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHERMAP_API_KEY}"
        )
        response.raise_for_status()
        if response.json():
            return response.json()[0]
        else:
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get city data: {str(e)}")
        return None


def get_weather_data(city_lat, city_lon, language, units):
    """
    Get weather forecast data for a given city from the OpenWeatherMap API.

    Parameters:
    - city_lat (float): The latitude of the city.
    - city_lon (float): The longitude of the city.
    - language (str): The language for the weather data.
    - units (str): The units for temperature measurement.

    Returns:
    dict: Weather forecast data for the specified city.
    """
    try:
        response = requests.get(
            f"{WEATHER_API_URL}/data/2.5/forecast?lat={city_lat}&lon={city_lon}&lang={language}&units={units}&appid={OPENWEATHERMAP_API_KEY}"
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get weather data: {str(e)}")
        return None


def format_forecast_data(forecast):
    """
    Format raw forecast data into a more readable format.

    Parameters:
    - forecast (dict): Raw forecast data from the OpenWeatherMap API.

    Returns:
    dict: Formatted forecast data including datetime, temperature, humidity, and more.
    """
    try:
        datetime_str = forecast.get("dt_txt", "")
        formatted_datetime = datetime.strptime(
            datetime_str, "%Y-%m-%d %H:%M:%S"
        ).strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        formatted_datetime = "N/A"

    main_data = forecast.get("main", {})

    temperature = main_data.get("temp")
    formatted_temperature = (
        f"{temperature}°C"
        if temperature is not None and isinstance(temperature, (int, float))
        else "N/A"
    )

    min_temperature = main_data.get("temp_min", 0)
    max_temperature = main_data.get("temp_max", 0)

    formatted_min_temperature = (
        f"{min_temperature}°C" if isinstance(min_temperature, (int, float)) else "N/A"
    )
    formatted_max_temperature = (
        f"{max_temperature}°C" if isinstance(max_temperature, (int, float)) else "N/A"
    )

    humidity = main_data.get("humidity", 0)
    formatted_humidity = f"{humidity}%" if isinstance(humidity, int) else "N/A"

    feels_like = main_data.get("feels_like", 0)
    formatted_feels_like = (
        f"{feels_like}°C" if isinstance(feels_like, (int, float)) else "N/A"
    )

    weather_description = forecast["weather"][0].get("description", "")
    formatted_weather_description = (
        weather_description.capitalize()
        if isinstance(weather_description, (str))
        else "N/A"
    )

    return {
        "datetime": formatted_datetime,
        "temperature": formatted_temperature,
        "min_temperature": formatted_min_temperature,
        "max_temperature": formatted_max_temperature,
        "humidity": formatted_humidity,
        "feels_like": formatted_feels_like,
        "weather_description": formatted_weather_description,
    }
