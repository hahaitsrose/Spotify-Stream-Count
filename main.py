import handlers.totphandler as totphand
from classes.album import Album as albobj
from classes.track import Track as trobj

metadata_link = input("Enter your link: ")
to_print = None

if "/album/" in metadata_link:
    obj = albobj(metadata_link)
    to_print = obj.get_streams()

elif "/track/" in metadata_link:
    obj = trobj(metadata_link)
    to_print = obj.get_streams()

else:
    to_print = "Potentially a bad link?"

print(to_print)

input()
