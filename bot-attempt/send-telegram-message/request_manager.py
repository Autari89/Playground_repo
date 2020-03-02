import json
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))
import requests

telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
api_url = f"https://api.telegram.org/bot{telegram_token}/"

class Request_manager:
    def __init__(self, sender_name:str, chat_id:str):
        self.sender_name = sender_name
        self.chat_id = chat_id

    def set_chat_text(self, text:str):
        self.chat_text = text

    def build_help_answer(self):
        self.final_message = "This is a help message, ask this Bot to translate something from english by writing translate:word_to_translate.\n\nYou can also ask for weather information, just type weather:city_to_check"

    def build_translate_answer(self):
        self.final_message = f'This answer is supposed to be related to translation'

    def build_weather_answer(self):
        self.final_message = "This answer is supposed to be related to weather"

    def process_request(self):
        if 'trans' in self.chat_text or 'Trans' in self.chat_text:
            self.build_translate_answer()
        elif 'weather' in self.chat_text or 'Weather' in self.chat_text:
            self.build_weather_answer()
        else:
            self.build_help_answer()

    def send_answer(self)->bool:
        params = {'chat_id': self.chat_id, 'text': self.final_message}
        res = requests.post(api_url + "sendMessage", data=params).json()
        return res