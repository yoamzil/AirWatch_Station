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
    
    # Greeting - expanded
    if any(word in message for word in ['hello', 'hi', 'hey', 'greetings', 'salam', 'good morning', 'good afternoon', 'good evening', 'howdy', 'sup', "what's up", 'yo']):
        return handle_greeting()
    
    # Current air quality - expanded
    elif any(word in message for word in ['current', 'now', 'today', 'right now', 'at the moment', 'currently', 'present', 'latest', 'air safe', 'air quality', 'how is the air', 'hows the air', 'breathe', 'outside now']):
        return handle_current_air_quality()
    
    # Historical data - MUCH MORE expanded
    elif any(phrase in message for phrase in [
        'yesterday', 'history', 'historical', 'past', 'last week', 'previous', 'before',
        'one hour ago', 'two hours ago', 'few hours ago', 'earlier', 'this morning', 'this afternoon',
        'last night', 'last month', 'past week', 'past month', 'ago', 'last time',
        'what was', 'how was', 'show me', 'data from', 'readings from', 'trend', 'trends',
        'over time', 'past data', 'historic', 'previous readings', 'old data'
    ]):
        return handle_historical_data()
    
    # Alerts - expanded
    elif any(word in message for word in ['alert', 'alerts', 'warning', 'warnings', 'anomaly', 'anomalies', 'problem', 'problems', 'issue', 'issues', 'notification', 'notifications', 'danger', 'critical', 'emergency']):
        return handle_alerts()
    
    # Health advice - MUCH MORE expanded
    elif any(phrase in message for phrase in [
        'running', 'run', 'jog', 'jogging', 'exercise', 'workout', 'outdoor', 'outdoors', 'outside',
        'children', 'child', 'kids', 'baby', 'babies',
        'safe', 'safety', 'should i', 'can i', 'is it safe', 'is it okay',
        'go out', 'going out', 'walk', 'walking', 'bike', 'biking', 'cycling',
        'play outside', 'open windows', 'open window', 'ventilate',
        'health', 'breathe', 'breathing', 'asthma', 'allergies',
        'recommendation', 'recommendations', 'advice', 'suggest', 'suggestion',
        'what should i do', 'what can i do', 'activity', 'activities'
    ]):
        return handle_health_advice()
    
    # Temperature specific - expanded
    elif any(word in message for word in ['temperature', 'temp', 'hot', 'cold', 'warm', 'cool', 'degrees', 'celsius', 'fahrenheit']):
        if any(phrase in message for phrase in ['yesterday', 'history', 'past', 'ago', 'last', 'previous', 'before', 'earlier']):
            return handle_historical_data()
        else:
            return handle_current_air_quality()
    
    # Humidity specific - new!
    elif any(word in message for word in ['humidity', 'humid', 'moisture', 'damp', 'dry']):
        if any(phrase in message for phrase in ['yesterday', 'history', 'past', 'ago', 'last', 'previous', 'before', 'earlier']):
            return handle_historical_data()
        else:
            return handle_current_air_quality()
    
    # AQI specific - new!
    elif any(word in message for word in ['aqi', 'air quality index', 'pollution', 'polluted']):
        if any(phrase in message for phrase in ['yesterday', 'history', 'past', 'ago', 'last', 'previous', 'before', 'earlier']):
            return handle_historical_data()
        else:
            return handle_current_air_quality()
    
    # Thanks/goodbye - new!
    elif any(word in message for word in ['thank', 'thanks', 'thank you', 'thx', 'appreciate', 'bye', 'goodbye', 'see you', 'later']):
        return "You're welcome! Feel free to ask me anything about air quality anytime. Stay safe! 👋"
    
    # Default response
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
    print("📡 Backend will be available at: http://localhost:5001")
    print("💡 Make sure your React app points to this URL")
    app.run(host='0.0.0.0', port=5001, debug=True)