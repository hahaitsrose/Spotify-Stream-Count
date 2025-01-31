import functions
import functions.albumfuncs
import functions.trackfuncs

data_link = input("Enter the link you wish to check (track or album)\n")

to_print = ""

if "/track/" in data_link:
    to_print = functions.trackfuncs.get_stream_count(data_link)
elif "/album/" in data_link:
    to_print = functions.albumfuncs.get_stream_count(data_link)
else:
    print(f"{data_link} is not a valid type to check for.")

print(to_print)

input()
