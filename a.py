import urllib.request

# URL of your online script
file = 'gem.py'
url = f'https://raw.githubusercontent.com/mitbingoo/robloxtools/main/{file}'

# Fetch the script content
response = urllib.request.urlopen(url)
script_content = response.read().decode('utf-8')

# Execute the script
exec(script_content)