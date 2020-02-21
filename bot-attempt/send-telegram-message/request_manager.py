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
        self.final_message = text

    def check_help_request(self)->bool:
        need_help = False
        if 'help' in self.chat_text:
            need_help = True
        return need_help

    def build_answer(self):
        need_help = self.check_help_request()
        if need_help:
            self.final_message = "This is a help message, ask this Bot to... with command \..."
        else:
            self.final_message = f'You just said:\n{self.chat_text}'

    def send_answer(self)->bool:
        params = {'chat_id': self.chat_id, 'text': self.final_message}
        res = requests.post(api_url + "sendMessage", data=params).json()
        return res