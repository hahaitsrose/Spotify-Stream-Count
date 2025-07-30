import json
from handlers import requestshandler as rqhand

class Album:
    def __init__(self, album_link):
        self.albumId = self.get_album_id(album_link)

    def get_album_id(self, album_link):
        base = album_link.split("?")[0]
        if "/album/" in base:
            return base.split("/album/")[1]
    
    def get_album_streams(self, limit=25, offset=0):
        params = {
            "operationName": "getAlbum",
            "variables": json.dumps(
                {
                    "locale": "",
                    "uri": f"spotify:album:{self.albumId}",
                    "offset": offset,
                    "limit": limit,
                }
            ),
            "extensions": json.dumps(
                {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "1a33c76ec27fc5cca497d8503c656cdea3641779300d33d5964a9858c87caafe",
                    }
                }
            ),
        }

        result = rqhand.get_web_request(params)
        return result
    
    def paginate_album(self):
        UPPER_LIMIT: int = 343
        album = self.get_album_streams(limit=UPPER_LIMIT)
        total_count: int = album["data"]["albumUnion"]["tracksV2"]["totalCount"]

        yield album["data"]["albumUnion"]["tracksV2"]["items"]

        if total_count <= UPPER_LIMIT:
            return

        offset = UPPER_LIMIT
        while offset < total_count:
            yield self.get_album_streams(limit=UPPER_LIMIT, offset=offset)["data"][
                "albumUnion"
            ]["tracksV2"]["items"]
            offset += UPPER_LIMIT


    def get_streams(self):
        counter = 0
        current_chunk = ""
        total_streams = 0
        gen = self.paginate_album()
        for batch in gen:
            for idx, item in enumerate(batch):
                counter += 1
                track = item['track']
                name = track['name']
                playcount = int(track['playcount'])
                total_streams += playcount
                line = f"{counter}. {name} : {playcount:,}\n"
                current_chunk += line

        average = f"{round(total_streams / counter):,}"
        total_streams = f"{total_streams:,}"
        current_chunk += f"\nTotal Streams: {total_streams} | Average: {average}"
        return current_chunk
