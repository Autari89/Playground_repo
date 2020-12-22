import json
from request_manager import Request_manager

request_manager = Request_manager()

def lambda_handler(event, context):
    field_errors = {}    # ignore event parameters other than these 3
    name = event['message']['chat']['first_name']
    text = event['message']['text']
    chat_id = event['message']['chat']['id']

    request_manager.clear_text()
    request_manager.set_sender_name(name)
    request_manager.set_chat_id(chat_id)
    request_manager.set_chat_text(text)
    request_manager.process_request()

    if field_errors:
        raise Exception(json.dumps({'field_errors': field_errors}))

    res = request_manager.send_answer()

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