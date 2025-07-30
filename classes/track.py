import json
from handlers import requestshandler as rqhand

class Track:
    def __init__(self, track_link):
        self.trackId = self.get_track_id(track_link)

    def get_track_id(self, track_link):
        base = track_link.split("?")[0]
        if "/track/" in base:
            return base.split("/track/")[1]

    def get_track_data(self):
        params = {
            "operationName": "getTrack",
            "variables": json.dumps(
                {
                    "uri": f"spotify:track:{self.trackId}",
                }
            ),
            "extensions": json.dumps(
                {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "26cd58ab86ebba80196c41c3d48a4324c619e9a9d7df26ecca22417e0c50c6a4",
                    }
                }
            ),
        }

        result = rqhand.get_web_request(params)
        return result

    def get_streams(self):
        data = self.get_track_data()
        track_info = data['data']['trackUnion']
        title = track_info['name']
        playcount = int(track_info['playcount'])
    
        album_of_track = track_info['albumOfTrack']
        visuals = album_of_track['coverArt']['sources'][0]['url']
        artist = track_info['firstArtist']['items'][0]['profile']['name']

        return f"{title} by {artist} : {playcount:,}"
