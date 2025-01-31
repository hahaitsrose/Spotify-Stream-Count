import requests, json
import functions
import functions.tokenfuncs

def get_stream_count(album_link):

    album_id = album_link
    if "/album/" in album_link:
        album_id = album_link.split("/album/")[1]
        if "?si=" in album_id:
            album_id = album_id.split("?si=")[0]
    else:
        return "That is an invalid link/id."

    token = functions.tokenfuncs.get_token()
    if token == False:
        return "There was an error fetching the data. Please try again in a moment."
    
    headers = {
            "Authorization": "Bearer " + token
            }
    params = {
            "operationName": "queryAlbumTracks",
            "variables": json.dumps({
                "uri": "spotify:album:" + album_id,
                "offset": 0,
                "limit": 50
            }),
            "extensions": json.dumps({
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "3ea563e1d68f486d8df30f69de9dcedae74c77e684b889ba7408c589d30f7f2e"
                }
            })
        }
    r_playcount = requests.get("https://api-partner.spotify.com/pathfinder/v1/query", headers=headers, params=params)
    if r_playcount.status_code == 200:
        r_playcount = r_playcount.json()

        counter = 0
        total_streams = 0
        string = ""

        for track in r_playcount["data"]["album"]["tracks"]["items"]:
            counter += 1
            track_info = track["track"]
            name = track_info["name"]
            playcount = int(track_info["playcount"])
            total_streams += playcount
            string += f"{counter}. {name}: {playcount:,}\n"
        string += f"Total: {total_streams:,}"
        return string
    else:
        return "There was an error fetching the data. Please try again in a moment."
