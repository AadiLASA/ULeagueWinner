import requests

API_KEY = "RGAPI-c6479b11-c413-4d9e-bc45-a4bcc76e4c25"  # Replace with your actual API key
summoner_name = "gatorniggilis"  # Your full summoner name
REGION = "na1"  # Change to your region if different

headers = {
    "X-Riot-Token": API_KEY
}

# Construct the URL
url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"

# Make the request
response = requests.get(url, headers=headers)

if response.status_code == 200:
    summoner_data = response.json()
    print(summoner_data)
else:
    print(f"Error: {response.status_code}, {response.text}")
