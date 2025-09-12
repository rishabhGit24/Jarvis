"""
Weather Information System for Jarvis
Provides real-time weather data and forecasts
"""
import requests
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import config

class JarvisWeather:
    def __init__(self):
        self.api_key = config.WEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.user_location = config.USER_LOCATION

    def get_current_weather(self, location: Optional[str] = None) -> Dict:
        """Get current weather for specified location or user's default location"""
        if not self.api_key:
            return {"error": "Weather API key not configured. Please set WEATHER_API_KEY in your .env file."}

        if location is None:
            location = self.user_location

        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': config.WEATHER_UNITS
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return self._format_current_weather(data)

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch weather data: {e}"}
        except Exception as e:
            return {"error": f"Weather service error: {e}"}

    def get_weather_forecast(self, location: Optional[str] = None, days: int = 5) -> Dict:
        """Get weather forecast for the next few days"""
        if not self.api_key:
            return {"error": "Weather API key not configured. Please set WEATHER_API_KEY in your .env file."}

        if location is None:
            location = self.user_location

        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': config.WEATHER_UNITS
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return self._format_forecast(data, days)

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch forecast data: {e}"}
        except Exception as e:
            return {"error": f"Forecast service error: {e}"}

    def _format_current_weather(self, data: Dict) -> Dict:
        """Format current weather data for display"""
        try:
            weather = data['weather'][0]
            main = data['main']
            wind = data.get('wind', {})

            # Temperature unit
            unit = "°C" if config.WEATHER_UNITS == 'metric' else "°F"

            formatted = {
                "location": f"{data['name']}, {data['sys']['country']}",
                "description": weather['description'].title(),
                "temperature": f"{main['temp']:.1f}{unit}",
                "feels_like": f"{main['feels_like']:.1f}{unit}",
                "humidity": f"{main['humidity']}%",
                "pressure": f"{main['pressure']} hPa",
                "visibility": f"{data.get('visibility', 0) / 1000:.1f} km" if 'visibility' in data else "N/A",
                "wind_speed": f"{wind.get('speed', 0):.1f} {'m/s' if config.WEATHER_UNITS == 'metric' else 'mph'}",
                "wind_direction": self._get_wind_direction(wind.get('deg', 0)),
                "cloudiness": f"{data['clouds']['all']}%",
                "sunrise": datetime.fromtimestamp(data['sys']['sunrise']).strftime("%H:%M"),
                "sunset": datetime.fromtimestamp(data['sys']['sunset']).strftime("%H:%M"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            return formatted

        except KeyError as e:
            return {"error": f"Invalid weather data format: missing {e}"}

    def _format_forecast(self, data: Dict, days: int) -> Dict:
        """Format forecast data for display"""
        try:
            forecasts = []
            current_date = None
            daily_data = {}

            unit = "°C" if config.WEATHER_UNITS == 'metric' else "°F"

            # Group forecasts by date
            for item in data['list'][:days * 8]:  # 8 forecasts per day (3-hour intervals)
                dt = datetime.fromtimestamp(item['dt'])
                date_str = dt.strftime("%Y-%m-%d")

                if date_str not in daily_data:
                    daily_data[date_str] = {
                        'date': dt.strftime("%A, %B %d"),
                        'temps': [],
                        'descriptions': [],
                        'humidity': [],
                        'wind_speeds': []
                    }

                daily_data[date_str]['temps'].append(item['main']['temp'])
                daily_data[date_str]['descriptions'].append(item['weather'][0]['description'])
                daily_data[date_str]['humidity'].append(item['main']['humidity'])
                daily_data[date_str]['wind_speeds'].append(item.get('wind', {}).get('speed', 0))

            # Create daily summaries
            for date_str, day_data in list(daily_data.items())[:days]:
                temps = day_data['temps']
                most_common_desc = max(set(day_data['descriptions']), key=day_data['descriptions'].count)

                forecast = {
                    'date': day_data['date'],
                    'high_temp': f"{max(temps):.1f}{unit}",
                    'low_temp': f"{min(temps):.1f}{unit}",
                    'description': most_common_desc.title(),
                    'avg_humidity': f"{sum(day_data['humidity']) / len(day_data['humidity']):.0f}%",
                    'avg_wind': f"{sum(day_data['wind_speeds']) / len(day_data['wind_speeds']):.1f} {'m/s' if config.WEATHER_UNITS == 'metric' else 'mph'}"
                }
                forecasts.append(forecast)

            return {
                "location": f"{data['city']['name']}, {data['city']['country']}",
                "forecasts": forecasts,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        except (KeyError, IndexError) as e:
            return {"error": f"Invalid forecast data format: {e}"}

    def _get_wind_direction(self, degrees: float) -> str:
        """Convert wind direction degrees to compass direction"""
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                     "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

        index = round(degrees / 22.5) % 16
        return directions[index]

    def get_weather_alerts(self, location: Optional[str] = None) -> Dict:
        """Get weather alerts for the location"""
        if not self.api_key:
            return {"error": "Weather API key not configured"}

        if location is None:
            location = self.user_location
        try:
            # First get coordinates
            geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {'q': location, 'appid': self.api_key, 'limit': 1}

            response = requests.get(geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            geo_data = response.json()

            if not geo_data:
                return {"error": "Location not found"}

            lat, lon = geo_data[0]['lat'], geo_data[0]['lon']

            # Get weather alerts using One Call API
            onecall_url = "https://api.openweathermap.org/data/3.0/onecall"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'exclude': 'minutely,hourly,daily'
            }

            response = requests.get(onecall_url, params=params, timeout=10)
            if response.status_code == 401:
                return {"message": "Weather alerts require a premium API key"}

            response.raise_for_status()
            data = response.json()

            alerts = data.get('alerts', [])
            if not alerts:
                return {"message": "No weather alerts for your location"}

            formatted_alerts = []
            for alert in alerts:
                formatted_alerts.append({
                    'title': alert.get('event', 'Weather Alert'),
                    'description': alert.get('description', ''),
                    'start': datetime.fromtimestamp(alert.get('start', 0)).strftime("%Y-%m-%d %H:%M"),
                    'end': datetime.fromtimestamp(alert.get('end', 0)).strftime("%Y-%m-%d %H:%M"),
                    'sender': alert.get('sender_name', 'Weather Service')
                })

            return {
                "location": location,
                "alerts": formatted_alerts,
                "count": len(formatted_alerts)
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch weather alerts: {e}"}
        except Exception as e:
            return {"error": f"Weather alerts service error: {e}"}

    def get_weather_summary(self, location: Optional[str] = None) -> str:
        """Get a natural language weather summary"""
        current = self.get_current_weather(location)

        if "error" in current:
            if "API key" in current["error"]:
                return "I apologize, Sir, but the weather service requires an API key to be configured. Please obtain a free API key from OpenWeatherMap and add it to your configuration."
            else:
                return f"I'm sorry, Sir, but I'm unable to retrieve weather information at the moment. {current['error']}"

        # Create natural language summary
        location_name = current["location"]
        temp = current["temperature"]
        desc = current["description"]
        feels_like = current["feels_like"]
        humidity = current["humidity"]
        wind = current["wind_speed"]

        summary = f"The current weather in {location_name} is {desc.lower()}. "
        summary += f"The temperature is {temp}, though it feels like {feels_like}. "
        summary += f"Humidity is at {humidity} with winds at {wind}. "

        # Add contextual advice
        temp_value = float(temp.replace('°C', '').replace('°F', ''))
        if config.WEATHER_UNITS == 'metric':
            if temp_value < 0:
                summary += "Quite cold out there, Sir. Do bundle up warmly."
            elif temp_value < 10:
                summary += "Rather chilly today, Sir. A jacket would be advisable."
            elif temp_value > 30:
                summary += "It's quite warm today, Sir. Perhaps stay hydrated."
        else:  # Fahrenheit
            if temp_value < 32:
                summary += "Freezing conditions, Sir. Do take care when venturing out."
            elif temp_value < 50:
                summary += "Rather cold today, Sir. Warm clothing recommended."
            elif temp_value > 85:
                summary += "Quite hot today, Sir. Do stay cool and hydrated."

        return summary

    def setup_weather_api(self) -> str:
        """Provide instructions for setting up weather API"""
        return """To enable weather functionality, please follow these steps:

1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Generate an API key
4. Create a .env file in the project directory with:
   WEATHER_API_KEY=your_api_key_here
   USER_LOCATION=your_city_name

The free tier provides:
- Current weather data
- 5-day weather forecast
- 1,000 API calls per day

This will enable me to provide you with comprehensive weather information, Sir."""
