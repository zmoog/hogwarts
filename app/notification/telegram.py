import requests


class TelegramNotifier:

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send(self, msg):
        params = {
            'chat_id': self.chat_id,
            'text': msg
        }
        r = requests.get(
            f'https://api.telegram.org/{self.token}/sendMessage',
            params=params
        )
