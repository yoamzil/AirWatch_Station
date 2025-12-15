import requests
from datetime import datetime, timedelta

# API Configuration
BASE_URL = "http://10.32.132.87:9090/api"
DEVICE_ID = "da8c8990-cfbc-11f0-8614-c1208bd774e4"
ACCESS_TOKEN = "dSsrQgsYBuAQHVfMfvmw"
USERNAME = "tenant@thingsboard.org"
PASSWORD = "tenant"

# Cache the JWT token to avoid getting it every time
_jwt_token = None
_token_expiry = None

def get_jwt_token():
    """
    Get JWT token for authenticated API calls.
    Caches the token to avoid unnecessary requests.
    """
    global _jwt_token, _token_expiry
    
    # Return cached token if still valid (tokens usually last 2 hours)
    if _jwt_token and _token_expiry and datetime.now() < _token_expiry:
        return _jwt_token
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": USERNAME, "password": PASSWORD},
            timeout=5
        )
        response.raise_for_status()
        
        _jwt_token = response.json()['token']
        # Set expiry to 1 hour from now (conservative)
        _token_expiry = datetime.now() + timedelta(hours=1)
        
        print("✅ JWT token obtained successfully")
        return _jwt_token
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting JWT token: {e}")
        return None

def get_current_readings():
    """
    Get the latest sensor readings from ThingsBoard.
    Returns: dict with temperature, humidity, and air_quality_index
    """
    try:
        # Get JWT token
        token = get_jwt_token()
        if not token:
            raise Exception("Failed to get authentication token")
        
        # Build the API endpoint
        endpoint = f"{BASE_URL}/plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries"
        params = {"keys": "temperature,humidity,airQuality"}
        headers = {"X-Authorization": f"Bearer {token}"}
        
        # Make the request
        response = requests.get(endpoint, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        print(f"📡 Raw API response: {data}")
        
        # Helper function to safely extract float values
        def safe_float(key, default=0.0):
            try:
                if key in data and data[key] and len(data[key]) > 0:
                    value = data[key][0].get('value')
                    if value is not None:
                        return float(value)
                return default
            except (ValueError, TypeError, KeyError, IndexError):
                return default
        
        # Parse the ThingsBoard response format
        result = {
            'temperature': safe_float('temperature', 23.5),
            'humidity': safe_float('humidity', 58.0),
            'air_quality_index': safe_float('airQuality', 45.0),
            'timestamp': None
        }
        
        # Try to get timestamp
        if 'temperature' in data and data['temperature'] and len(data['temperature']) > 0:
            result['timestamp'] = data['temperature'][0].get('ts')
        
        # Check if we got real data
        has_real_data = any([
            'temperature' in data and data['temperature'],
            'humidity' in data and data['humidity'],
            'airQuality' in data and data['airQuality']
        ])
        
        if not has_real_data:
            result['error'] = 'No sensor data available'
            print("⚠️ No sensor data found - using default values")
        else:
            print(f"✅ Current readings retrieved: Temp={result['temperature']}°C, "
                  f"Humidity={result['humidity']}%, airQuality={result['air_quality_index']}")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching current readings: {e}")
        return {
            'temperature': 22.0,
            'humidity': 45.0,
            'air_quality_index': 42.0,
            'timestamp': None,
            'error': 'Using dummy data - API unavailable'
        }
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {
            'temperature': 0,
            'humidity': 0,
            'air_quality_index': 0,
            'timestamp': None,
            'error': str(e)
        }
        
        print(f"✅ Current readings retrieved: Temp={result['temperature']}°C, "
              f"Humidity={result['humidity']}%, airQuality={result['air_quality_index']}")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching current readings: {e}")
        # Return dummy data for testing when API is unavailable
        return {
            'temperature': 22.0,
            'humidity': 45.0,
            'air_quality_index': 42.0,
            'timestamp': None,
            'error': 'Using dummy data - API unavailable'
        }
    
    except (KeyError, IndexError, ValueError) as e:
        print(f"❌ Error parsing sensor data: {e}")
        return {
            'temperature': 0,
            'humidity': 0,
            'air_quality_index': 0,
            'timestamp': None,
            'error': 'Data parsing error'
        }

def get_historical_data(days=7):
    """
    Get historical sensor data from ThingsBoard.
    
    Args:
        days: Number of days of history to retrieve (default: 7)
    
    Returns: list of readings with date, temperature, humidity, and airQuality
    """
    try:
        # Get JWT token
        token = get_jwt_token()
        if not token:
            raise Exception("Failed to get authentication token")
        
        # Calculate time range (ThingsBoard uses milliseconds)
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        
        # Build the API endpoint
        endpoint = f"{BASE_URL}/plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries"
        params = {
            "keys": "temperature,humidity,airQuality",
            "startTs": start_time,
            "endTs": end_time
        }
        headers = {"X-Authorization": f"Bearer {token}"}
        
        # Make the request
        response = requests.get(endpoint, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Parse and combine the data
        readings = []
        
        # Get all timestamps from temperature data
        if 'temperature' in data and data['temperature']:
            temp_data = {item['ts']: float(item['value']) for item in data['temperature']}
            humid_data = {item['ts']: float(item['value']) for item in data.get('humidity', [])}
            airQuality_data = {item['ts']: float(item['value']) for item in data.get('airQuality', [])}
            
            # Combine data by timestamp
            for ts in sorted(temp_data.keys(), reverse=True):
                readings.append({
                    'timestamp': ts,
                    'date': datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M'),
                    'temperature': temp_data.get(ts, 0),
                    'humidity': humid_data.get(ts, 0),
                    'air_quality_index': airQuality_data.get(ts, 0)
                })
        
        print(f"✅ Retrieved {len(readings)} historical readings")
        return readings[:50]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching historical data: {e}")
        return [
            {
                'date': 'Yesterday',
                'temperature': 20.0,
                'humidity': 50.0,
                'air_quality_index': 38.0
            },
            {
                'date': '2 days ago',
                'temperature': 21.0,
                'humidity': 48.0,
                'air_quality_index': 42.0
            }
        ]

def get_alerts():
    """
    Check for anomalies/alerts in recent data.
    """
    try:
        recent_data = get_historical_data(days=1)
        alerts = []
        
        for reading in recent_data:
            airQuality = reading.get('air_quality_index', 0)
            temp = reading.get('temperature', 0)
            
            if airQuality > 100:
                alerts.append({
                    'timestamp': reading.get('date', 'Unknown'),
                    'type': 'High airQuality',
                    'message': f"Air quality reached unhealthy levels (airQuality: {airQuality})",
                    'severity': 'warning' if airQuality < 150 else 'critical'
                })
            
            if temp > 35:
                alerts.append({
                    'timestamp': reading.get('date', 'Unknown'),
                    'type': 'High Temperature',
                    'message': f"Temperature exceeded 35°C ({temp}°C)",
                    'severity': 'warning'
                })
        
        seen = set()
        unique_alerts = []
        for alert in alerts:
            key = f"{alert['type']}_{alert['timestamp']}"
            if key not in seen:
                seen.add(key)
                unique_alerts.append(alert)
        
        return unique_alerts[:10]
    
    except Exception as e:
        print(f"❌ Error checking for alerts: {e}")
        return []

if __name__ == "__main__":
    print("🔍 Testing API connection...")
    token = get_jwt_token()
    if token:
        print(f"✅ Authentication successful!")
        current = get_current_readings()
        print(f"✅ Current readings: {current}")
    else:
        print("❌ Authentication failed!")