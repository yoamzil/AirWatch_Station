def get_health_recommendation(aqi):
    """
    Provide health recommendations based on Air Quality Index
    """
    
    if aqi <= 50:
        return """✅ **Air Quality: GOOD**

• Perfect for all outdoor activities
• Great time for exercise and sports
• Safe for children to play outside
• No health precautions needed
• Enjoy your day! 🌟"""
    
    elif aqi <= 100:
        return """☁️ **Air Quality: MODERATE**

• Generally safe for most people
• Unusually sensitive individuals should consider limiting prolonged outdoor exertion
• Perfect for normal outdoor activities
• Keep windows open for fresh air"""
    
    elif aqi <= 150:
        return """⚠️ **Air Quality: UNHEALTHY FOR SENSITIVE GROUPS**

• Sensitive groups (children, elderly, those with respiratory conditions) should limit prolonged outdoor exertion
• General public can still enjoy outdoor activities
• Consider indoor exercise if you're sensitive
• Monitor symptoms if you have asthma or heart disease"""
    
    elif aqi <= 200:
        return """🚨 **Air Quality: UNHEALTHY**

• Everyone should reduce prolonged outdoor exertion
• Sensitive groups should avoid outdoor activities
• Close windows and use air purifiers
• Wear a mask (N95) if you must go outside
• Reschedule outdoor events if possible"""
    
    elif aqi <= 300:
        return """🛑 **Air Quality: VERY UNHEALTHY**

• Everyone should avoid all outdoor physical activities
• Stay indoors with windows closed
• Use air purifiers if available
• Sensitive groups should remain indoors
• Seek medical attention if experiencing symptoms"""
    
    else:
        return """☢️ **Air Quality: HAZARDOUS**

⚠️ HEALTH WARNING: Emergency conditions

• Everyone MUST avoid all outdoor activities
• Stay indoors with air filtration
• Do not open windows or doors
• Evacuate if advised by authorities
• Seek immediate medical attention for any respiratory distress"""