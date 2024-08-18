import sys
import subprocess
import importlib
import concurrent.futures
version = "1.1.1"
def install_requests():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

# Check if requests is installed, if not, install it
try:
    importlib.import_module("requests")
except ImportError:
    print("requests module not found. Installing...")
    install_requests()

import requests

def fetch_id():
    response = requests.get("https://raw.githubusercontent.com/mitbingoo/robloxtools/main/account/userid.txt")
    return response.text.splitlines()

def process_id(id, url, max_retries=3):
    url_formatted = url.format(id)
    response = None
    retry_count = 0
    while retry_count < max_retries:
        if response is None or "error" in response.text.lower() or "false" in response.text.lower():
            print(f"Retrying request for id: {id} (Retry {retry_count+1}/{max_retries})")
            response = requests.get(url_formatted)
            retry_count += 1
        else:
            break
    print(f"Processed line: {id}, Response: {response.text}")

def process_ids_concurrently(ids, url, max_workers=5):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_id, id, url) for id in ids]
        concurrent.futures.wait(futures)

def main():
    apis = {
    "1": "https://shouko-api.neyoshiiuem.workers.dev/bypass?link=https://gateway.platoboost.com/a/8?id={}&api_key=mitbingoapikeyreal",
    "2": "https://stickx.top/api-delta/?hwid={}&api_key=E99l9NOctud3vmu6bPne"
    }

    print(f"Delta v{version} - by @mitbingoo")
    print("==============================================")
    print("Available APIs:")

    for api, url in apis.items():
        print(f"API: {api} - URL: {url}")
    api_mode = input("Choose API: ")
    url = apis[api_mode]

    while True:
        try:
            ids = fetch_id()
            process_ids_concurrently(ids, url)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()