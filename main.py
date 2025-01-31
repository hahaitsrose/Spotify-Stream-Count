import functions
import functions.albumfuncs
import functions.trackfuncs

data_link = input("Enter the link you wish to check (track or album)\n")
album_or_single = input("Album or Track?\n")
album_or_single_lower = album_or_single.lower()

to_print = ""

if album_or_single_lower == "track":
    to_print = functions.trackfuncs.get_stream_count(data_link)
elif album_or_single_lower == "album":
    to_print = functions.albumfuncs.get_stream_count(data_link)
else:
    print(f"{album_or_single_lower} is not a valid type to check for.")

print(to_print)

input()
