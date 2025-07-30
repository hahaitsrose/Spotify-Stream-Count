import requests
from classes.a_token import Token as tkobj

def get_web_request(params):
    url = "https://api-partner.spotify.com/pathfinder/v1/query"
    req_tok = tkobj()
    headers = {
            "Authorization": "Bearer " + req_tok.get_token()
            }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
