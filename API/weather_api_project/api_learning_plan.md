# 🌤️ API Programming Learning Plan (Beginner)

This hands-on guide will teach you the fundamentals of REST APIs using **Python**, **VS Code**, and **Postman**. We will pull live weather forecasts using the completely free, no-signup [National Weather Service API](https://weather.gov).

---

## 🛠️ Step 1: Environment Setup

Before writing code, let's set up the professional toolkit.

### 1. Install Python & VS Code
1. Download and install [Python](https://python.org). *Crucial:* During installation, ensure you check the box that says **"Add python.exe to PATH"**.
2. Download and install [Visual Studio Code](https://code.visualstudio.com/).
3. Open VS Code, click the **Extensions icon** on the left menu bar (or press `Ctrl+Shift+X`), search for **Python** (by Microsoft), and click install.

### 2. Set Up Postman
Instead of installing a separate application, you can use Postman directly within your code editor!
1. In the VS Code Extensions tab, search for **Postman**.
2. Install the [Postman VS Code Extension](https://learning.postman.com/docs/reference/vs-code-extension/overview).
3. Look for the Postman icon on your left sidebar, click it, and sign in to a free account.

---

## 🚀 Step 2: Testing the API in Postman (No Code Yet)

Before writing code, we always use a client like Postman to test how an API responds. The NWS API requires two steps: first, lookup your latitude and longitude to get your specific "Grid Endpoint," then request the forecast from that grid.

### The First Request: Grid Lookup
1. Open the **Postman extension** in VS Code and create a new **HTTP Request**.
2. Set the HTTP request method dropdown to **GET**.
3. In the URL bar, paste this address (this example uses the coordinates for Washington, D.C.):
    `https://api.weather.gov/points/38.9072,-77.0369`
4. Click **Send**.
5. Look at the JSON response at the bottom. Scroll down to find the `properties` block and locate the `forecast` URL. It will look like this: 
    The response contains a `properties.forecast` URL, such as `https://api.weather.gov/gridpoints/LWX/...`.

### The Second Request: Fetch the Live Weather
1. Copy that `forecast` URL from your response body.
2. Create a **New HTTP Request** in Postman.
3. Paste that forecast URL into the address bar and click **Send**.
4. You will receive a rich JSON structure containing the current forecast, temperatures, and wind speeds!

---

## 🐍 Step 3: Writing the Python Implementation

Now, let's translate what we did in Postman into a repeatable Python script inside VS Code.

### 1. Create your Project Folder
1. Create a folder on your computer named `weather_api_project`.
2. Open VS Code, go to `File > Open Folder`, and select your new folder.
3. Create a new file by hitting `Ctrl+N`, and save it immediately as `weather.py`.

### 2. Install the Request Library
APIs require an HTTP client library. In Python, the industry standard is `requests`.
1. Open your integrated terminal in VS Code (`View > Terminal` or press `Ctrl+``).
2. Run the following command to install the package:
   ```bash
   pip install requests
   ```

### 3. Write the Code
Paste the following code into your `weather.py` file:

```python
import requests

def get_weather():
    # Step 1: Define our coordinates (Latitude, Longitude)
    # The National Weather Service requires a 'User-Agent' header so they know who is calling their data.
    headers = {
        'User-Agent': 'MyWeatherApp/1.0 (contact@example.com)'
    }
    
    # Coordinates for Washington, D.C. Change these to your own coordinates!
    points_url = "https://api.weather.gov/points/38.9072,-77.0369"
    
    print("Connecting to the Weather API...")
    
    # Step 2: Make the initial metadata request
    response = requests.get(points_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Step 3: Extract the specific forecast URL from the JSON payload
        forecast_url = data['properties']['forecast']
        
        # Step 4: Make the actual forecast request
        forecast_response = requests.get(forecast_url, headers=headers)
        
        if forecast_response.status_code == 200:
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
        else:
            print(f"Failed to fetch forecast details. Status code: {forecast_response.status_code}")
    else:
        print(f"Failed to fetch metadata points. Status code: {response.status_code}")

if __name__ == "__main__":
    get_weather()
```

### 4. Run the Code
1. Save your changes (`Ctrl+S`).
2. Click the **Play button** in the top right corner of VS Code, or type `python weather.py` in your terminal window.
3. Watch your terminal print out a clean, live weather forecast parsed entirely from a web API!

---

## 🧠 Key Core API Concepts to Remember

* **HTTP GET:** The method used to retrieve data from a server without modifying anything.
* **Status Code 200:** The universal internet standard code for "OK" / Request Successful. 
* **JSON (JavaScript Object Notation):** The data format returned by the weather server (and most web APIs) that organizes data into readable `key: value` pairs.
* **Headers:** Metadata sent alongside your request. In this project, `User-Agent` acts as our application signature.
