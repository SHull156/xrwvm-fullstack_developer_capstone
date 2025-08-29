import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url',
    default="http://localhost:3030"
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default=(
        "https://sentianalyzer.1zlbgu0pcp4y.us-south.codeengine."
        "appdomain.cloud/"
    )
)


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += key + "=" + value + "&"

    request_url = backend_url + endpoint + "?" + params
    print("GET from {} ".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Network exception occurred: {err}")
        return None


def analyze_review_sentiments(text):
    base_url = sentiment_analyzer_url.rstrip("/")
    request_url = base_url + "/analyze/" + text
    try:
        response = requests.get(request_url)
        if response.status_code == 200:
            return response.json()
        print(f"Analyzer returned status {response.status_code}")
        return {"sentiment": "unknown"}
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return {"sentiment": "unknown"}


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as err:
        print(f"Network exception occurred: {err}")
        return None
