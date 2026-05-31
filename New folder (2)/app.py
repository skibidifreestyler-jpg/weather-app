
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

API_KEY = "9a8e66a5a64e3f65f4b58517db502ebe"

@app.route("/weather")
def weather():
    city = request.args.get("city")

    current = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    ).json()

    if current.get("cod") != 200:
        return jsonify({"error": current.get("message","error")})

    forecast_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
    ).json()

    # hourly (next 8 results ~ 24h)
    hourly = []
    for i in range(0,8):
        item = forecast_data["list"][i]
        hourly.append({
            "time": item["dt_txt"].split(" ")[1][:5],
            "temp": round(item["main"]["temp"])
        })

    # daily grouping
    days = {}
    for item in forecast_data["list"]:
        day = item["dt_txt"].split(" ")[0]
        if day not in days:
            days[day] = {
                "temps": [],
                "weather": item["weather"][0]["main"]
            }
        days[day]["temps"].append(item["main"]["temp"])

    forecast = []
    for d in list(days.keys())[:5]:
        forecast.append({
            "day": d,
            "temp": round(sum(days[d]["temps"]) / len(days[d]["temps"])),
            "weather": days[d]["weather"]
        })

    return jsonify({
        "city": city,
        "weather": current["weather"][0]["main"],
        "temperature": round(current["main"]["temp"]),
        "humidity": current["main"]["humidity"],
        "wind": current["wind"]["speed"],
        "feels_like": round(current["main"]["feels_like"]),
        "forecast": forecast,
        "hourly": hourly
    })

if __name__ == "__main__":
    app.run(debug=True)
