import os
from typing import Final, Optional

import requests

BASE_URL: Final[str] = (
    "https://api.openweathermap.org/data/2.5/weather"
)

DEFAULT_CITY: Final[str] = "Karachi"
REQUEST_TIMEOUT: Final[int] = 10


def build_weather_params(city: str, api_key: str) -> dict[str, str]:
    """
    Build API request parameters.
    """

    return {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }


def format_weather_response(data: dict, city: str) -> str:
    """
    Format weather API response into readable text.
    """

    main_data = data.get("main", {})
    weather_data = data.get("weather", [{}])[0]
    wind_data = data.get("wind", {})

    temperature = main_data.get("temp", "N/A")
    feels_like = main_data.get("feels_like", "N/A")
    humidity = main_data.get("humidity", "N/A")
    pressure = main_data.get("pressure", "N/A")

    description = (
        weather_data.get("description", "Unknown")
        .capitalize()
    )

    wind_speed = wind_data.get("speed", "N/A")

    return (
        f"Weather in {city}:\n"
        f"• Temperature: {temperature}°C\n"
        f"• Feels Like: {feels_like}°C\n"
        f"• Condition: {description}\n"
        f"• Humidity: {humidity}%\n"
        f"• Pressure: {pressure} hPa\n"
        f"• Wind Speed: {wind_speed} m/s"
    )


def get_weather(city: Optional[str] = DEFAULT_CITY) -> str:
    """
    Fetch current weather data for a city
    using the OpenWeatherMap API.
    """

    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        return (
            "Error: WEATHER_API_KEY is missing.\n"
            "Please configure it in your .env file."
        )

    city = (city or DEFAULT_CITY).strip().title()

    params = build_weather_params(city, api_key)

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        # API-specific validation
        if str(data.get("cod")) != "200":
            message = data.get("message", "Unknown error")

            return (
                f"Weather lookup failed: "
                f"{message.capitalize()}."
            )

        return format_weather_response(data, city)

    except requests.Timeout:
        return (
            "The weather service took too long to respond. "
            "Please try again later."
        )

    except requests.ConnectionError:
        return (
            "Unable to connect to the weather service. "
            "Check your internet connection."
        )

    except requests.HTTPError as error:
        status_code = (
            error.response.status_code
            if error.response
            else "Unknown"
        )

        return (
            f"Weather API returned an HTTP error "
            f"(status: {status_code})."
        )

    except requests.RequestException as error:
        return f"Weather request failed: {error}"

    except ValueError:
        return "Failed to decode weather service response."

    except Exception as error:
        return f"Unexpected error: {error}"
