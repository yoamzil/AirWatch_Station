# API Documentation

MAKE SURE TO CONNECT TO 1337_GUEST!!!!

## Base URL
```
http://localhost:9090/api
```

## Authentication
Use device access token in URL or header.

---

## Send Sensor Data

**Endpoint:** `POST /v1/{ACCESS_TOKEN}/telemetry`

**Example:**
```bash
curl -X POST http://localhost:9090/api/v1/YOUR_TOKEN/telemetry \
  -H "Content-Type: application/json" \
  -d '{"temperature":23.5,"humidity":58,"aqi":45}'
```

---

## Get Current Data

**Endpoint:** `GET /plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries?keys=temperature,humidity,aqi`

**Example:**
```bash
curl http://localhost:9090/api/plugins/telemetry/DEVICE/YOUR_DEVICE_ID/values/timeseries?keys=temperature,humidity,aqi
```

**Response:**
```json
{
  "temperature": [{"ts": 1701234567890, "value": "23.5"}],
  "humidity": [{"ts": 1701234567890, "value": "58"}],
  "aqi": [{"ts": 1701234567890, "value": "45"}]
}
```

---

## Get Historical Data

**Endpoint:** `GET /plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries?keys=temperature&startTs={START}&endTs={END}`

**Example (Last 24 hours):**
```bash
START=$(($(date +%s) - 86400))000
END=$(date +%s)000

curl "http://localhost:9090/api/plugins/telemetry/DEVICE/YOUR_DEVICE_ID/values/timeseries?keys=temperature,humidity,aqi&startTs=$START&endTs=$END"
```

---

## For Team Integration

### Module 3 (Analyst)
Use historical data endpoint to fetch data for anomaly detection.

### Module 4 (AI Assistant)
Use current data endpoint to provide context for AI responses.

**JavaScript Example:**
```javascript
const fetchData = async () => {
  const response = await fetch(
    'http://localhost:9090/api/plugins/telemetry/DEVICE/YOUR_DEVICE_ID/values/timeseries?keys=temperature,humidity,aqi'
  );
  return response.json();
};
```