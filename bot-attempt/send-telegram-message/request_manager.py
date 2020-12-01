import json
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))
import requests

telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
app_id = os.environ['OXFORD_APP_ID']
app_key = os.environ['OXFORD_APP_KEY']
api_url = f"https://api.telegram.org/bot{telegram_token}/"
language = 'en-gb'
dic_api_url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/'  + language + '/'

headers = {
    'app_id': f"{app_id}",
    'app_key': f"{app_key}"
}

class Request_manager:
    def __init__(self, sender_name: str, chat_id: str):
        self.sender_name = sender_name
        self.chat_id = chat_id
        self.final_message = []

    def set_chat_text(self, text: str):
        self.chat_text = text

    def build_help_answer(self):
        self.final_message = "This is a help message, ask this Bot to translate something from english by writing translate:word_to_translate.\n\nYou can also ask for weather information, just type weather:city_to_check"

    def build_translate_answer(self):
        word_to_translate = self.chat_text.split(":")
        new_url = dic_api_url + word_to_translate[1].strip()
        response = requests.get(new_url, headers=headers)
        response_data = response.json()
        index = 1

        for sense in response_data['results'][0]['lexicalEntries'][0]['entries'][0]['senses']:
            definition = "Definition " + f'{index}' + ": " + sense['definitions'][0]
            self.final_message.append(f'{definition}')
            index = index + 1

    def build_weather_answer(self):
        self.final_message = "This answer is supposed to be related to weather"

    def process_request(self):
        if 'trans' in self.chat_text or 'Trans' in self.chat_text:
            self.build_translate_answer()
        elif 'weather' in self.chat_text or 'Weather' in self.chat_text:
            self.build_weather_answer()
        else:
            self.build_help_answer()

    def send_answer(self) -> bool:
        overall_message = ""

        for message in self.final_message:
            overall_message = overall_message + message + "\n\n"

        params = {'chat_id': self.chat_id, 'text': overall_message}
        res = requests.post(api_url + "sendMessage", data=params).json()
        return res