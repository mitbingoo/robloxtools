import sys
import subprocess
import importlib
import concurrent.futures
import time
version = "1.2.1"

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

def process_id(id, url, max_retries=5):
    url_formatted = url.format(id)
    response = None
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = requests.get(url_formatted)
            if "error" not in response.text.lower() and "false" not in response.text.lower():
                break
            print(f"Retrying request for id: {id} (Retry {retry_count+1}/{max_retries})")
            retry_count += 1
        except requests.RequestException:
            print(f"Request failed for id: {id} (Retry {retry_count+1}/{max_retries})")
            retry_count += 1
        time.sleep(1)  # Add a small delay between retries
    
    result = response.text if response else "Failed to get response"
    print(f"Processed line: {id}, Response: {result}")
    return id, result

def process_ids_concurrently(ids, url, batch_size=10):
    with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
        for i in range(0, len(ids), batch_size):
            batch = ids[i:i+batch_size]
            futures = [executor.submit(process_id, id, url) for id in batch]
            results = concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
            
            for future in results.done:
                id, result = future.result()
                print(f"Completed processing for id: {id}")
            
            print(f"Batch of {len(batch)} requests completed.")
            time.sleep(2)  # Add a delay between batches to avoid overwhelming the server

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