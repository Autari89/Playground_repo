import unittest
import os
import sys

os.environ["TELEGRAM_BOT_TOKEN"] = "TELEGRAM_BOT_TOKEN"
os.environ["OXFORD_APP_ID"] = "OXFORD_APP_ID"
os.environ["OXFORD_APP_KEY"] = "OXFORD_APP_KEY"
sys.path.append('bot-attempt/send-telegram-message')

from request_manager import Request_manager

class TestRequestManager(unittest.TestCase):
    def setUp(self):
        self.request_manager = Request_manager()

    def test_constructor(self):
        self.assertEqual(None, self.request_manager.sender_name)
        self.assertEqual(None, self.request_manager.chat_id)
    
    def test_setter_funtions(self):
        sender_name = "Sender"
        chat_id = "Chat id"
        chat_text = "A chat text"

        self.request_manager.set_sender_name(sender_name)
        self.request_manager.set_chat_id(chat_id)
        self.request_manager.set_chat_text(chat_text)
        
        self.assertEqual(sender_name, self.request_manager.sender_name)
        self.assertEqual(chat_id, self.request_manager.chat_id)
        self.assertEqual(chat_text, self.request_manager.chat_text)

if __name__ == '__main__':
    unittest.main()