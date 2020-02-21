import json
import os
import sys
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))
import requests

telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
api_url = f"https://api.telegram.org/bot{telegram_token}/"

def check_help_request(body:str)->bool:
    need_help = False
    if 'help' in body:
        need_help = True
    return need_help

def build_answer(body_text:str, need_help:bool)->str:
    if need_help:
        final_message = "This is a help message, ask this Bot to... with command \..."
    else:
        final_message = f'You just said:\n{body_text}'
    return final_message

def send_answer(chat_id:str, telegram_msg:str):
    params = {'chat_id': chat_id, 'text': telegram_msg}
    res = requests.post(api_url + "sendMessage", data=params).json()
    return res

def lambda_handler(event, context):
    field_errors = {}    # ignore event parameters other than these 3
    name = event['message']['chat']['first_name']
    text = event['message']['text']
    chat_id = event['message']['chat']['id']

    telegram_msg = build_answer(text, check_help_request(text))

    if field_errors:
        raise Exception(json.dumps({'field_errors': field_errors}))

    res = send_answer(chat_id, telegram_msg)

    if res["ok"]:
        return {
            'statusCode': 200,
            'body': res['result'],
        }
    else:
        print(res)
        return {
            'statusCode': 400,
            'body': res
        }