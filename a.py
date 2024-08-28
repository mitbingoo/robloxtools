import subprocess
import sys
import time
import requests

def install_request():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

try:
    import requests
except ImportError:
    print("Requests module not found. Installing...")
    install_request()
    import requests

def get_password():
    url = "https://raw.githubusercontent.com/mitbingoo/robloxtools/main/backup/ps.txt"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        print("Failed to retrieve password.")
        sys.exit(1)

correct_password = get_password()

while True:
    user_password = input("Enter the password: ")
    if user_password == correct_password:
        break
    else:
        print("Incorrect password. Please try again.")

print("Password correct. Downloading and executing script...")

file = 'gem.py'
url = f'https://raw.githubusercontent.com/mitbingoo/robloxtools/main/{file}'

max_attempts = 2
attempt = 0

while attempt < max_attempts:
    try:
        response = requests.get(url)
        response.raise_for_status()
        code = response.text
        
        print(f"Successfully downloaded {file}")
        print("Executing the script...")
        
        exec(code)
        break
    except requests.RequestException as e:
        print(f"Error downloading the script: {e}")
    except Exception as e:
        print(f"Error executing script: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
        attempt += 1

if attempt == max_attempts:
    print("Failed to execute the script after multiple attempts.")