# API Documentation

⚠️ **IMPORTANT: Connect to 1337_GUEST WiFi!**

## Configuration

```bash
BASE_URL="http://10.32.132.87:9090/api"
DEVICE_ID="da8c8990-cfbc-11f0-8614-c1208bd774e4"
ACCESS_TOKEN="dSsrQgsYBuAQHVfMfvmw"
USERNAME="tenant@thingsboard.org"
PASSWORD="tenant"
```

---

## Authentication

### Get JWT Token
```bash
TOKEN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])" | tr -d '\n')
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

## Get Current Data (Latest Telemetry)

**Endpoint:** `GET /plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries?keys=temperature,humidity,aqi`

**Example:**
```bash
# Step 1: Get JWT token
TOKEN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])" | tr -d '\n')

# Step 2: Get latest telemetry
curl -X GET "$BASE_URL/plugins/telemetry/DEVICE/$DEVICE_ID/values/timeseries?keys=temperature,humidity,aqi" \
  -H "X-Authorization: Bearer $TOKEN"
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
# Step 1: Get JWT token
TOKEN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])" | tr -d '\n')

# Step 2: Calculate time range
START=$(($(date +%s) - 86400))000
END=$(date +%s)000

# Step 3: Get historical data
curl -X GET "$BASE_URL/plugins/telemetry/DEVICE/$DEVICE_ID/values/timeseries?keys=temperature,humidity,aqi&startTs=$START&endTs=$END" \
  -H "X-Authorization: Bearer $TOKEN"
```

---

## Quick Reference

| Endpoint | Method | Auth | Use Case |
|----------|--------|------|----------|
| `POST /v1/{TOKEN}/telemetry` | POST | Token in URL | Send sensor data |
| `GET /plugins/telemetry/DEVICE/{ID}/values/timeseries` | GET | JWT in header | Get latest readings |
| `GET /plugins/telemetry/DEVICE/{ID}/values/timeseries?startTs=...&endTs=...` | GET | JWT in header | Get historical data |

---

## For Team Integration

### Module 3 (Analyst)
Use historical data endpoint for anomaly detection.

### Module 4 (AI Assistant)
Use latest telemetry endpoint for current readings.
