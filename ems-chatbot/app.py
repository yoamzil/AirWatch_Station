from flask import Flask, request, jsonify
from flask_cors import CORS
from api_client import get_current_readings, get_historical_data, get_alerts
from health_advisor import get_health_recommendation

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the React frontend"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        response = process_message(user_message)
        
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'response': f"Sorry, I encountered an error: {str(e)}"
        }), 500

def process_message(message):
    """Process the user's message and return appropriate response"""
    message = message.lower()
    
    if any(word in message for word in ['hello', 'hi', 'hey', 'greetings', 'salam']):
        return handle_greeting()
    elif any(word in message for word in ['current', 'now', 'today', 'air safe', 'air quality']):
        return handle_current_air_quality()
    elif any(word in message for word in ['yesterday', 'history', 'historical', 'past', 'last week', 'previous']):
        return handle_historical_data()
    elif any(word in message for word in ['alert', 'warning', 'anomaly', 'problem', 'issue']):
        return handle_alerts()
    elif any(word in message for word in ['running', 'exercise', 'outdoor', 'children', 'safe', 'should i', 'can i']):
        return handle_health_advice()
    elif 'temperature' in message:
        if any(word in message for word in ['yesterday', 'history', 'past']):
            return handle_historical_data()
        else:
            return handle_current_air_quality()
    else:
        return handle_default()

def handle_greeting():
    return """Hello! 👋 I'm your environmental health assistant.

I can help you with:
• Current air quality and sensor readings
• Historical data and trends
• Health recommendations based on conditions
• Alerts and anomalies

What would you like to know?"""

def handle_current_air_quality():
    try:
        data = get_current_readings()
        
        if 'error' in data:
            return f"⚠️ I'm having trouble accessing the sensors right now.\n\nMake sure you're connected to the 1337_GUEST WiFi network.\n\nTest data: Temp {data['temperature']}°C, Humidity {data['humidity']}%, AQI {data['air_quality_index']}"
        
        temp = data['temperature']
        humidity = data['humidity']
        aqi = data['air_quality_index']
        
        response = "🌡️ **Current Environmental Readings**\n\n"
        response += f"🌡️ Temperature: {temp}°C\n"
        response += f"💧 Humidity: {humidity}%\n"
        response += f"🌬️ Air Quality Index: {aqi}\n\n"
        
        if aqi < 50:
            response += "✅ **Air quality is excellent!**\nPerfect for all outdoor activities. 🌟"
        elif aqi < 100:
            response += "☁️ **Air quality is moderate.**\nGenerally safe for most people."
        elif aqi < 150:
            response += "⚠️ **Unhealthy for sensitive groups.**\nSensitive individuals should limit prolonged outdoor activity."
        else:
            response += "🚨 **Air quality is unhealthy.**\nConsider limiting outdoor exposure."
        
        return response
    except Exception as e:
        return f"Sorry, I couldn't retrieve current readings. Error: {str(e)}"

def handle_historical_data():
    try:
        data = get_historical_data(days=2)
        
        if not data:
            return "I couldn't find any historical data. The sensors might be newly set up. Try asking about current conditions instead!"
        
        response = "📊 **Recent Environmental History**\n\n"
        
        for entry in data[:5]:
            date = entry.get('date', 'Unknown')
            temp = entry.get('temperature', 0)
            humidity = entry.get('humidity', 0)
            aqi = entry.get('air_quality_index', 0)
            
            response += f"**{date}**\n"
            response += f"  • Temperature: {temp}°C\n"
            response += f"  • Humidity: {humidity}%\n"
            response += f"  • AQI: {aqi}\n\n"
        
        if len(data) > 5:
            response += f"_(Showing 5 of {len(data)} recent readings)_"
        
        return response
    except Exception as e:
        return f"Sorry, I couldn't retrieve historical data. Error: {str(e)}"

def handle_alerts():
    try:
        alerts = get_alerts()
        
        if not alerts or len(alerts) == 0:
            return "✅ **Good news!**\n\nNo air quality alerts detected in the last 24 hours. All systems are running normally."
        
        response = f"⚠️ **Found {len(alerts)} Alert(s)**\n\n"
        
        for alert in alerts[:5]:
            timestamp = alert.get('timestamp', 'Unknown time')
            alert_type = alert.get('type', 'Alert')
            message = alert.get('message', 'No details')
            severity = alert.get('severity', 'info')
            
            emoji = "⚠️" if severity == "warning" else "🚨"
            response += f"{emoji} **{alert_type}**\n"
            response += f"  • Time: {timestamp}\n"
            response += f"  • {message}\n\n"
        
        if len(alerts) > 5:
            response += f"_(Showing 5 of {len(alerts)} alerts)_"
        
        return response
    except Exception as e:
        return f"Sorry, I couldn't check for alerts. Error: {str(e)}"

def handle_health_advice():
    try:
        data = get_current_readings()
        aqi = data['air_quality_index']
        
        advice = get_health_recommendation(aqi)
        
        response = f"🏥 **Health Advisory**\n\n"
        response += f"Current Air Quality Index: **{aqi}**\n\n"
        response += advice
        
        return response
    except Exception as e:
        return f"Sorry, I couldn't generate health advice right now. Error: {str(e)}"

def handle_default():
    return """I'm not sure what you're asking about. Here's what I can help with:

💬 **Try asking:**
• "Is the air safe right now?"
• "What was the temperature yesterday?"
• "Any alerts today?"
• "Should I go running?"
• "Give me health recommendations"

What would you like to know?"""

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Chatbot API is running'})

if __name__ == '__main__':
    print("🚀 Starting EMS Chatbot Backend...")
    print("📡 Backend will be available at: http://localhost:5000")
    print("💡 Make sure your React app points to this URL")
    app.run(host='0.0.0.0', port=5000, debug=True)