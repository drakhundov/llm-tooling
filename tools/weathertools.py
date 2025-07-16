import os

import requests

from tooling import agent_tool

WEATHER_API_URL = (
        "https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid="
        + os.getenv("WEATHER_API_TOKEN")
)


@agent_tool
def get_current_weather_info(location: str) -> str:
    """Tells the most recent weather information at a specified location."""
    try:
        info = requests.get(WEATHER_API_URL.format(location=location)).json()
        desc = info["weather"][0]["description"]
        temp = info["main"]["temp"]
        status = (
                "It is "
                + desc
                + " in "
                + " ".join([i.capitalize() for i in location.split(" ")])
                + " now.\n"
        )
        status += "Temperature now is " + str(temp) + " degrees.\n"
        if temp > 25:
            status += "Wear shorts (or skirt) and a T-shirt."
        elif temp > 10:
            status += "Wear a coat."
        else:
            status += "It's very cold. Wear jacket."
    except Exception as e:
        status = "City is not recognized"
    return status
