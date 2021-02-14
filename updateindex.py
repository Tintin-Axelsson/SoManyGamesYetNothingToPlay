import requests
import json

r = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
data = r.json()

with open('appid_index.json', 'w') as f:
    f.write(json.dumps(data, indent=4, sort_keys=True))
