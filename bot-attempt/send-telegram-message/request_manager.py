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
dic_api_url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/'  + language + '/word_id?fields=definitions&strictMatch=false'

headers = {
    'app_id': f"{app_id}",
    'app_key': f"{app_key}"
}

class Request_manager:
    def __init__(self, sender_name = None, chat_id = None):
        self.sender_name = sender_name
        self.chat_id = chat_id
        self.final_message = []
        self.new_url = []
        self.show_translation = False
        self.help_message_active = False
        self.expect_pronunciation = False

    def set_sender_name(self,  sender_name: str):
        self.sender_name = sender_name
    
    def set_chat_id(self, chat_id: str):
        self.chat_id = chat_id

    def set_chat_text(self, text: str):
        self.chat_text = text

    def build_help_answer(self):
        self.final_message.append("This is a help message, ask this Bot to translate something from english by writing translate:word_to_translate.\n\nYou can also ask for weather information, just type weather:city_to_check")

    def build_translate_answer(self):
        self.show_translation = True
        word_to_translate = self.chat_text.split(":")
        self.new_url = dic_api_url.replace("word_id", word_to_translate[1].strip())
        response = requests.get(self.new_url, headers=headers)
        response_data = response.json()
        index = 1

        for sense in response_data['results'][0]['lexicalEntries'][0]['entries'][0]['senses']:
            definition = "Definition " + f'{index}' + ": " + sense['definitions'][0]
            self.final_message.append(f'{definition}')
            index = index + 1

    def build_weather_answer(self):
        self.final_message.append("This answer is supposed to be related to weather")

    def ask_pronunciation(self, is_positive_answer: bool):
        if is_positive_answer:
            new_url = self.new_url.replace("definitions", "pronunciations")
            response = requests.get(new_url, headers=headers)
            pronunciation = response.json()['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']
            self.final_message.append(f'{pronunciation}')
        else:
            self.expect_pronunciation = False
        

    def process_request(self):
        if 'trans' in self.chat_text or 'Trans' in self.chat_text:
            self.build_translate_answer()
        elif 'weather' in self.chat_text or 'Weather' in self.chat_text:
            self.build_weather_answer()
        elif ('Yes' in self.chat_text or 'No' in self.chat_text) and self.expect_pronunciation:
            is_positive_answer = 'Yes' in self.chat_text 
            self.ask_pronunciation(is_positive_answer)
        else:
            self.help_message_active = True
            self.build_help_answer()

    def send_answer(self) -> bool:
        overall_message = ""

        if self.help_message_active:
            overall_message = self.final_message
            self.help_message_active = False
        elif self.expect_pronunciation:
            overall_message = self.final_message
            self.expect_pronunciation = False
        elif self.show_translation:
            for message in self.final_message:
                overall_message = overall_message + message + "\n\n"
            overall_message = overall_message + "Do you want to listen the pronunciation?"
            self.expect_pronunciation = True
            self.show_translation = False

        params = {'chat_id': self.chat_id, 'text': overall_message}
        res = requests.post(api_url + "sendMessage", data=params).json()
        return res

    def clear_text(self):
        self.final_message = []
