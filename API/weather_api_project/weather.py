import requests

def get_weather():
    # Step 1: Define our coordinates (Latitude, Longitude)
    # The National Weather Service requires a 'User-Agent' header so they know who is calling their data.
    headers = {
        'User-Agent': 'MyWeatherApp/1.0 (contact@example.com)',
        'Accept': 'application/geo+json'
    }
    
    # Coordinates for Washington, D.C. Change these to your own coordinates!
    #points_url = "https://api.weather.gov/points/38.9072,-77.0369"
    points_url = "https://api.weather.gov/points/34.1207,-84.0043"
    
    print("Connecting to the Weather API...")
    
    # Step 2: Make the initial metadata request
    try:
        response = requests.get(points_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Step 3: Extract the specific forecast URL from the JSON payload
        forecast_url = data['properties']['forecast']
        
        # Step 4: Make the actual forecast request
        forecast_response = requests.get(forecast_url, headers=headers, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # Step 5: Extract the upcoming forecast periods
        periods = forecast_data['properties']['periods']

        print("\n--- Live 3-Day Weather Forecast ---")
        # Loop through the first 6 periods (Day/Night cycles for 3 days)
        for period in periods[:6]:
            name = period['name']
            temperature = period['temperature']
            unit = period['temperatureUnit']
            detailed_forecast = period['detailedForecast']

            print(f"\n👉 {name}: {temperature}°{unit}")
            print(f"   {detailed_forecast}")
    except requests.exceptions.RequestException as error:
        print(f"Weather API request failed: {error}")
    except ValueError as error:
        print(f"Weather API returned invalid JSON: {error}")

if __name__ == "__main__":
    get_weather()
