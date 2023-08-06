import requests


class Rasa:
    def __init__(self, onedash_token):
        self.token = onedash_token

    def log_data(self, data):
        url = 'https://app.onedash.cc/api/insert/record/rasa'
        headers = {'Authorization': self.token}
        response = requests.post(url=url, headers=headers, json=data)

    @classmethod
    def from_endpoint_config(
            cls, broker_config
    ):
        if broker_config is None:
            return None
        return cls(**broker_config.kwargs)

    def publish(self, event):
        if event['event'] in ('user', 'bot'):
            self.log_data(event)
