import requests
import json

def fetch_new_secret():
    response = requests.get("https://github.com/Thereallo1026/spotify-secrets/blob/main/secrets/secretDict.json?raw=true")
    secrets = response.json()

    latest_secret = secrets[(v := max(secrets, key=int))]

    return v, latest_secret