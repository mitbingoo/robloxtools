import sys
import subprocess
import importlib

def install_requests():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

# Check if requests is installed, if not, install it
try:
    importlib.import_module("requests")
except ImportError:
    print("requests module not found. Installing...")
    install_requests()

import requests
import time

def fetch_id():
    response = requests.get("https://r.mitmc.top/")
    return response.text.splitlines()

def process_ids(ids, url):
    for id in ids:
        url_formatted = url.format(id)
        response = requests.get(url_formatted)
        print(f"Processed line: {id}, Response: {response.text}")

def main():
    apis = {
    "1": "https://shouko-api.neyoshiiuem.workers.dev/bypass?link=https://gateway.platoboost.com/a/8?id={}&api_key=mitbingoapikeyreal",
    "2": "https://stickx.top/api-delta/?hwid={}&api_key=E99l9NOctud3vmu6bPne"
    }

    for api, url in apis.items():
        print(f"API: {api} - URL: {url}")
    api_mode = input("Choose API: ")
    url = apis[api_mode]

    while True:
        try:
            ids = fetch_id()
            process_ids(ids, url)
        except Exception as e:
            print(f"An error occurred: {e}")
        

if __name__ == "__main__":
    main()