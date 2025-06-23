import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

class GoogleSearchAgent:
    def __init__(self, api_key, cx_id):
        self.api_key = api_key
        self.cx = cx_id

    def search(self, query):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "safe": "off"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            print("Ошибка:", data["error"]["message"])
            return []

        results = data.get("items", [])
        for i, item in enumerate(results, 1):
            print(f"{i}. {item['title']}\n{item['link']}\n")

        return results


agent = GoogleSearchAgent(api_key=api_key, cx_id="00d92e72f2da44f8b")
agent.search("как работает трансформер в NLP")
