import unittest
from unittest.mock import patch, Mock
import requests
from functions.aux_functions import (
    get_city_data,
    get_weather_data,
    format_forecast_data,
)
import app


class TestGetCityData(unittest.TestCase):
    @patch("functions.aux_functions.requests.get")
    def test_successful_response(self, mock_get):
        expected_result = {"lat": 123, "lon": 456, "name": "CityName"}
        mock_response = Mock()
        mock_response.json.return_value = [expected_result]
        mock_get.return_value = mock_response

        result = get_city_data("CityName")
        self.assertEqual(result, expected_result)

    @patch("functions.aux_functions.requests.get")
    def test_get_city_data_failure(self, mock_get):
        mock_get.return_value.json.return_value = []

        city_data = get_city_data("Invalid City")

        self.assertIsNone(city_data)


class TestGetWeatherData(unittest.TestCase):
    @patch("functions.aux_functions.requests.get")
    def test_successful_response(self, mock_get):
        expected_result = {
            "list": [
                {
                    "dt_txt": "2022-01-01 12:00:00",
                    "main": {
                        "temp": 25,
                        "temp_min": 20,
                        "temp_max": 30,
                        "humidity": 80,
                        "feels_like": 23,
                    },
                    "weather": [{"description": "cloudy"}],
                }
            ]
        }
        mock_response = Mock()
        mock_response.json.return_value = expected_result
        mock_get.return_value = mock_response

        result = get_weather_data(123, 456, "en", "metric")
        self.assertEqual(result, expected_result)

    @patch("functions.aux_functions.requests.get")
    def test_get_weather_data_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        city_lat = 51.5074
        city_lon = -0.1278
        language = "en"
        units = "metric"
        result = get_weather_data(city_lat, city_lon, language, units)

        self.assertIsNone(result)


class TestFormatForecastData(unittest.TestCase):
    def test_valid_forecast_data(self):
        forecast = {
            "dt_txt": "2023-01-01 12:00:00",
            "main": {
                "temp": 25,
                "temp_min": 20,
                "temp_max": 30,
                "humidity": 80,
                "feels_like": 23,
            },
            "weather": [{"description": "cloudy"}],
        }

        expected_result = {
            "datetime": "01/01/2023 12:00:00",
            "temperature": "25°C",
            "min_temperature": "20°C",
            "max_temperature": "30°C",
            "humidity": "80%",
            "feels_like": "23°C",
            "weather_description": "Cloudy",
        }

        result = format_forecast_data(forecast)
        self.assertEqual(result, expected_result)

    def test_invalid_forecast_data(self):
        forecast = {
            "dt_txt": "2023-01-01 12:00:00",
            "main": {
                "temp": None,
                "temp_min": None,
                "temp_max": None,
                "humidity": None,
                "feels_like": None,
            },
            "weather": [{"description": None}],
        }

        expected_result = {
            "datetime": "01/01/2023 12:00:00",
            "temperature": "N/A",
            "min_temperature": "N/A",
            "max_temperature": "N/A",
            "humidity": "N/A",
            "feels_like": "N/A",
            "weather_description": "N/A",
        }

        result = format_forecast_data(forecast)
        self.assertEqual(result, expected_result)


class TestGetWeather(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_get_weather_success(self):
        response = self.client.get("/weather?city=Brasilia&language=pt_br&units=metric")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("city_name", data)
        self.assertIn("forecasts", data)

    def test_get_weather_invalid_city(self):
        response = self.client.get(
            "/weather?city=InvalidCity&language=pt_br&units=metric"
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Failed to get city data")


class TestGetRequests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_get_previous_requests(self):
        response = self.client.get("/requests")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_get_previous_requests_with_query_params(self):
        response = self.client.get(
            "/requests?start_date=2022-01-01&end_date=2022-01-31&city=London&language=en&units=metric"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_get_previous_requests_with_invalid_dates(self):
        response = self.client.get(
            "/requests?start_date=2022-01-01&end_date=2021-12-31"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json, [])

    def test_get_previous_requests_with_invalid_city(self):
        response = self.client.get("/requests?city=NonexistentCity")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json, [])


if __name__ == "__main__":
    unittest.main()
