import os
import requests

def get_weather(city="Karachi"):
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key or api_key == "your_openweathermap_api_key_here":
        return "Error: Weather API key is missing. Please update your .env file."

    if not city:
        city = "Karachi" # Default fallback

    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(base_url)
        data = response.json()
        
        if data["cod"] != 200:
            return f"Sorry, I couldn't find the weather for {city}."
            
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"The current weather in {city} is {temp}°C with {description}."
        
    except Exception as e:
        return "I'm having trouble connecting to the weather service right now."