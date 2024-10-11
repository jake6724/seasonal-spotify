from SpotifyTool import SpotifyTool
from AlbumDataTool import AlbumDataTool
from Album import Album

"""
TODO: Fix variable names... some too generic some too specific
"""

SPT = SpotifyTool()

# SPT.get_album("Kendrick Lamar", "good kid, m.A.A.d city")

ADT = AlbumDataTool()
invalid_albums = []

# # Generate album list from Billboard Top 200 csv
album_list = ADT.process_album_data()
print(album_list)

# # Iterate through album list, search for each album with Spotify API
size = len(album_list)
for i, album_data in enumerate(album_list):
	print(f"({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]}")
	album_obj = SPT.get_album(album_data[0], album_data[1])
	print(album_obj)
	if not album_obj:
		print("Album not valid\n")
		invalid_albums.append(f"{album_data[0]}, {album_data[1]}")

print(f"Invalid albums: {invalid_albums}")
print(f"Invalid album count: {len(invalid_albums)}")