from SpotifyTool import SpotifyTool
from AlbumDataTool import AlbumDataTool
from Album import Album

"""
TODO: Fix variable names... some too generic some too specific
"""

SPT = SpotifyTool()
ADT = AlbumDataTool()
invalid_album_count = 0

# # Generate album list from Billboard Top 200 csv
album_list = ADT.process_album_data()

# # Iterate through album list, search for each album with Spotify API
for album_data in album_list:
	print(f"Artist: {album_data[0]}, {album_data[1]}")
	album_obj = SPT.get_album(album_data[0], album_data[1])
	print(album_obj)
	if not album_obj:
		print("Album not valid")
		invalid_album_count += 1

print(f"Invalid album count: {invalid_album_count}")