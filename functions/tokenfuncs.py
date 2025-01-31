import requests

def get_token():
    r_token = requests.get("https://open.spotify.com/get_access_token?reason=transport&productType=web_player")
    if r_token.status_code == 200:
        r_token = r_token.json()
        token = r_token["accessToken"]
        return token
    else:
        return False
