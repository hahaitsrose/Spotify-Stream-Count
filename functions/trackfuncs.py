import requests, json
import functions
import functions.tokenfuncs

def get_stream_count(track_link):

    track_id = track_link
    if "/track/" in track_link:
        track_id = track_link.split("/track/")[1]
        if "?si=" in track_id:
            track_id = track_id.split("?si=")[0]
    else:
        return "Incorrect link."
    
    token = functions.tokenfuncs.get_token()
    if token == False:
        return "There was an error fetching the data. Please try again in a moment."
    
    headers = {
                "Authorization": "Bearer " + token
            }
    params = {
                "operationName": "getTrack",
                "variables": json.dumps({
                    "uri": "spotify:track:" + track_id,
                }),
                "extensions": json.dumps({
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "e101aead6d78faa11d75bec5e36385a07b2f1c4a0420932d374d89ee17c70dd6"
                    }
                })
            }
    track_data = requests.get("https://api-partner.spotify.com/pathfinder/v1/query", headers=headers, params=params)
    if track_data.status_code == 200:
        track_data = track_data.json()

        trackUnion = track_data["data"]['trackUnion']
        title = trackUnion['name']
        playcount = int(trackUnion['playcount'])

        return f"{title}: {playcount:,}"
    else:
        return "There was an error fetching the data. Please try again in a moment."
