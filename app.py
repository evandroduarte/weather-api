import os
import re
from bson import json_util
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from utils.db import init_collection
from utils.logger_startup import logger
from functions.aux_functions import (
    get_city_data,
    get_weather_data,
    format_forecast_data,
)

app = Flask(__name__)

collection = init_collection()


@app.route("/weather", methods=["GET"])
def get_weather():
    """
    Get weather forecast for a specified city and store the data in the database.

    Args:
    - city (str): The name of the city.
    - language (str): The language for the weather data.
    - units (str): The units for temperature measurement.

    Returns:
    jsonify: JSON response containing the city name and forecast data.
    """
    try:
        city = request.args.get("city", default="Brasilia", type=str)
        language = request.args.get("language", default="pt_br", type=str)
        units = request.args.get("units", default="metric", type=str)

        city_data = get_city_data(city)

        if not city_data:
            return jsonify({"error": "Failed to get city data"}), 500

        city_lat, city_lon, city_name = (
            city_data.get("lat"),
            city_data.get("lon"),
            city_data.get("name"),
        )

        weather_data = get_weather_data(city_lat, city_lon, language, units)

        if not weather_data:
            return jsonify({"error": "Failed to get weather data"}), 500

        daily_forecast = [
            format_forecast_data(forecast) for forecast in weather_data.get("list", [])
        ]

        collection.insert_one(
            {
                "city": city,
                "language": language,
                "units": units,
                "forecast": daily_forecast,
                "timestamp": datetime.now(),
            }
        )

        return jsonify({"city_name": city_name, "forecasts": daily_forecast}), 200

    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/requests", methods=["GET"])
def get_previous_requests():
    """
    Get previous weather requests based on specified query parameters.

    Args:
    - start_date (str): The start date for the query (YYYY-MM-DD).
    - end_date (str): The end date for the query (YYYY-MM-DD).
    - city (str): The name of the city.
    - language (str): The language for the weather data.
    - units (str): The units for temperature measurement.

    Returns:
    Response: JSON response containing the requested weather data.
    """
    try:
        query_params = request.args.to_dict()

        start_date_str = query_params.pop("start_date", None)
        end_date_str = query_params.pop("end_date", None)

        start_date = (
            datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
        )
        end_date = (
            datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1)
            if end_date_str
            else None
        )

        query_params = {
            key.lower(): value.lower() for key, value in query_params.items()
        }

        city_query = (
            {
                "city": {
                    "$regex": re.escape(query_params.get("city", "")),
                    "$options": "i",
                }
            }
            if query_params.get("city")
            else {}
        )
        query_params.update(city_query)

        date_query = (
            {"timestamp": {"$gte": start_date, "$lt": end_date}}
            if start_date and end_date
            else {}
        )
        query_params.update(date_query)

        result = collection.find(query_params)
        serialized_result = json_util.dumps(list(result))

        return serialized_result, 200, {"Content-Type": "application/json"}

    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=True)
