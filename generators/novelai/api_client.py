from config import CONFIG
import requests

BASE_PATH = "https://api.novelai.net/"

class NovelAIAPIClient:
    def __init__(self, access_token):
        self._access_token = access_token
    def _request(self, path, verb="GET", json=None, data=None):
        return requests.request(verb, json=json, data=data, headers={"Authorization": "Bearer " + self._access_token, "Content-Type": "application/json"}, url=BASE_PATH + path).json()
    def subscription(self):
        return self._request("user/subscription")
    def generate(self, model_input, model, parameters):
        return self._request("ai/generate", "POST", {"input": model_input, "model": model, "parameters": parameters})

api = NovelAIAPIClient(CONFIG["novelai"]["access_token"])

# print(api.generate("SCQ=", "6B", {"temperature": 0.8, "min_length": 10, "max_length": 20}))