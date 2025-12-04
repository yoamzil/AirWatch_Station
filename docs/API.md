# API Documentation

⚠️ **IMPORTANT: Connect to 1337_GUEST WiFi!**

## Configuration

```bash
BASE_URL="http://10.32.132.87:9090/api"
DEVICE_ID="your_device_id_here"
ACCESS_TOKEN="your_access_token_here"
```

---

## Send Sensor Data (Telemetry)

**Endpoint:** `POST /v1/{ACCESS_TOKEN}/telemetry`

**Example:**
```bash
curl -X POST $BASE_URL/v1/$ACCESS_TOKEN/telemetry \
  -H "Content-Type: application/json" \
  -d '{"temperature":23.5,"humidity":58,"aqi":45}'
```

---

## Get Latest Telemetry (Current Readings)

**Endpoint:** `GET /v1/{ACCESS_TOKEN}/telemetry?keys=temperature,humidity,aqi`

**Example:**
```bash
# Get latest sensor values
curl $BASE_URL/v1/$ACCESS_TOKEN/telemetry?keys=temperature,humidity,aqi
```

**Response:**
```json
{
  "temperature": [{"ts": 1701234567890, "value": 23.5}],
  "humidity": [{"ts": 1701234567890, "value": 58}],
  "aqi": [{"ts": 1701234567890, "value": 45}]
}
```

---

## Get Attributes (Device Configuration)

**Endpoint:** `GET /v1/{ACCESS_TOKEN}/attributes?clientKeys=key1&sharedKeys=key2`

**Example:**
```bash
# Get device attributes
curl $BASE_URL/v1/$ACCESS_TOKEN/attributes?clientKeys=location&sharedKeys=firmware
```

**Response:**
```json
{
  "client": {"location": "Room A"},
  "shared": {"firmware": "1.0.0"}
}
```

---

## Get Historical Data

**Endpoint:** `GET /plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries?keys=temperature&startTs={START}&endTs={END}`

**Example (Last 24 hours):**
```bash
START=$(($(date +%s) - 86400))000
END=$(date +%s)000

curl "$BASE_URL/plugins/telemetry/DEVICE/$DEVICE_ID/values/timeseries?keys=temperature,humidity,aqi&startTs=$START&endTs=$END"
```

---

## Quick Reference

| Need | Endpoint | Use Case |
|------|----------|----------|
| **Current sensor data** | `GET /v1/{TOKEN}/telemetry?keys=...` | Get latest readings |
| **Send sensor data** | `POST /v1/{TOKEN}/telemetry` | Upload new readings |
| **Device config** | `GET /v1/{TOKEN}/attributes` | Get device settings |
| **Historical data** | `GET /plugins/telemetry/DEVICE/{ID}/values/timeseries` | Get time-series data |

---

## For Team Integration

### Module 3 (Analyst)
Use historical data endpoint for anomaly detection.

### Module 4 (AI Assistant)
Use latest telemetry endpoint for current readings.

**JavaScript Example:**
```javascript
const BASE_URL = 'http://10.32.132.87:9090/api';
const ACCESS_TOKEN = 'your_access_token_here';

// Get latest readings
const getCurrentData = async () => {
  const response = await fetch(
    `${BASE_URL}/v1/${ACCESS_TOKEN}/telemetry?keys=temperature,humidity,aqi`
  );
  return response.json();
};

// Get historical data
const getHistoricalData = async (hours = 24) => {
  const DEVICE_ID = 'your_device_id_here';
  const endTs = Date.now();
  const startTs = endTs - (hours * 60 * 60 * 1000);
  
  const response = await fetch(
    `${BASE_URL}/plugins/telemetry/DEVICE/${DEVICE_ID}/values/timeseries?keys=temperature,humidity,aqi&startTs=${startTs}&endTs=${endTs}`
  );
  return response.json();
};
```