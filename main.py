import requests
import os
from twilio.rest import Client

OWM_Endpoint = 'https://api.openweathermap.org/data/3.0/onecall?'
api_key = os.getenv('OWM_API')
account_sid = os.environ['twilio_sid']
auth_token = os.environ['twilio_token']


weather_params = {
    'lat': 24.147736,
    'lon': 120.673645,
    'appid': api_key,
    'exclude': 'current,minutely,daily'
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
print(weather_data)
weather_slice = weather_data['hourly'][:12]

will_rain = False
for hour_data in weather_slice:
    weather_code = hour_data['weather'][0]['id']
    if int(weather_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body='bring an umbrella☔️',
        from_=os.getenv("email"),
        to=os.getenv("emailTo")
    )
    print(message.status)
