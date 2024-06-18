from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

API_KEY = "b730b74322cb6f19c4cdac22fdd822f7"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

@app.get("/weather")
async def get_weather(city: str):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="City not found or API error")

    data = response.json()
    forecast_list = data['list']
    forecast = {}

    for item in forecast_list:
        date = item['dt_txt'].split(" ")[0]
        if date not in forecast:
            forecast[date] = {
                'humidity': item['main']['humidity'],
                'temperature': item['main']['temp'],
                'wind_speed': item['wind']['speed'],
                'precipitation': item.get('pop', 0)  # 'pop' might be absent sometimes
            }

    return forecast

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)