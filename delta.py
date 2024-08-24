import sys
import subprocess
import importlib
import concurrent.futures
import time
version = "1.3.0"

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

def process_id(id, url, max_retries):
    url_formatted = url.format(id)
    response = None
    for retry_count in range(max_retries):
        print(f"Processing: {id} (Attempt {retry_count+1}/{max_retries})")
        sys.stdout.flush()
        try:
            response = requests.get(url_formatted)
            if "error" not in response.text.lower() and "false" not in response.text.lower():
                break
        except requests.RequestException:
            pass
    
    result = response.text if response else "Failed to get response"
    if response and "error" not in response.text.lower() and "false" not in response.text.lower():
        print(f"Done: {id}")
    else:
        print(f"Failed: {id}, {result}")
    sys.stdout.flush()
    return id, result

def process_ids_concurrently(ids, url, batch_size, max_retries):
    with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
        for i in range(0, len(ids), batch_size):
            batch = ids[i:i+batch_size]
            futures = [executor.submit(process_id, id, url, max_retries) for id in batch]
            results = concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
            
            for future in results.done:
                id, result = future.result()
            print("==============================================")

def main():
    apis = {
    "1": "https://shouko-api.neyoshiiuem.workers.dev/bypass?link=https://gateway.platoboost.com/a/8?id={}&api_key=mitbingoapikeyreal",
    "2": "https://stickx.top/api-delta/?hwid={}&api_key=E99l9NOctud3vmu6bPne"
    "3": "http://103.176.24.132:9000/delta/bypass?link=https://gateway.platoboost.com/a/8?id={}"
    }

    print(f"Delta v{version} - by @mitbingoo")
    print("==============================================")
    print("Available APIs:")

    for api, url in apis.items():
        print(f"API: {api} - URL: {url}")
    api_mode = input("Choose API: ")
    url = apis[api_mode]

    # Ask user for batch size
    while True:
        try:
            batch_size = int(input("Enter the batch size (number of concurrent requests): "))
            if batch_size > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")
    # Ask user for number of retries
    while True:
        try:
            max_retries = int(input("Enter the maximum number of retries: "))
            if max_retries > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")        

    while True:
        try:
            ids = fetch_id()
            process_ids_concurrently(ids, url, batch_size, max_retries)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()