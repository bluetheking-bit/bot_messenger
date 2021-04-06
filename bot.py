import random
import os

import requests
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
VERIFY_TOKEN = 'MYVerifyToken21'

bot = Bot(ACCESS_TOKEN)


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get('hub.verify_token')
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_weather()
                    send_message(recipient_id, response_sent_text)
        return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else:
        return 'Invalid verification token'


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return 'Success'


def get_message():
    sample_responses = ["Awesome!", "I like it!", "Very good!",
                        "Best, I've ever seen!"]
    return random.choice(sample_responses)


def get_weather():
    city = "293396"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city, 'units': 'metric', 'lang': 'ru', 'APPID': os.getenv('APPID')})
        data = res.json()
        return f"Weather is {data['main']['temp']} °C"
    except Exception as e:
        print("Exception (find):", e)
        pass


if __name__ == '__main__':
    app.run()
