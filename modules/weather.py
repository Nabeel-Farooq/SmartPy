import os
from typing import Optional

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_CITY = "Karachi"
REQUEST_TIMEOUT = 10


def get_weather(city: Optional[str] = DEFAULT_CITY) -> str:
    """
    Fetch current weather data for a city using OpenWeatherMap API.
    """

    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        return (
            "Error: WEATHER_API_KEY is missing. "
            "Please configure it in your .env file."
        )

    city = (city or DEFAULT_CITY).strip()

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        # Raise exception for HTTP errors
        response.raise_for_status()

        data = response.json()

        # API-specific validation
        if str(data.get("cod")) != "200":
            message = data.get("message", "Unknown error")
            return f"Weather lookup failed: {message.capitalize()}."

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].capitalize()

        return (
            f"Weather in {city}:\n"
            f"• Temperature: {temperature}°C\n"
            f"• Feels Like: {feels_like}°C\n"
            f"• Condition: {description}\n"
            f"• Humidity: {humidity}%"
        )

    except requests.Timeout:
        return "The weather service took too long to respond."

    except requests.ConnectionError:
        return "Unable to connect to the weather service."

    except requests.HTTPError as error:
        return f"HTTP error occurred: {error}"

    except requests.RequestException as error:
        return f"Request failed: {error}"

    except Exception as error:
        return f"Unexpected error: {error}"
