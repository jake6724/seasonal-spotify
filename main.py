from SpotifyTool import SpotifyTool
from AlbumDataTool import AlbumDataTool
from Album import Album

"""
TODO: Fix variable names... some too generic some too specific
"""

SPT = SpotifyTool()

SPT.get_album("Kendrick Lamar", "good kid, m.A.A.d city")

ADT = AlbumDataTool()
invalid_albums_1 = []
invalid_albums_2 = []
invalid_albums_3 = []

# # Generate album list from Billboard Top 200 csv
album_list = ADT.process_album_data()
print(album_list)

# # Iterate through album list, search for each album with Spotify API
size = len(album_list)
for i, album_data in enumerate(album_list):
	print(f"({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]}")
	result = SPT.get_album(album_data[0], album_data[1])
	# print(result[0])
	if result[1] == 1:
		print("Album Invalid\n")
		invalid_albums_1.append(f"{album_data[0]}, {album_data[1]}, return code: {result[1]}")
	elif result[1] == 2:
		print("Album Invalid\n")
		invalid_albums_2.append(f"{album_data[0]}, {album_data[1]}, return code: {result[1]}")
	elif result[1] == 3:
		print("Album Invalid\n")
		invalid_albums_3.append(f"{album_data[0]}, {album_data[1]}, return code: {result[1]}")

print(f"Invalid albums 1: {invalid_albums_1}")
print(f"Invalid albums 2: {invalid_albums_2}")
print(f"Invalid albums 3: {invalid_albums_3}")
print(f"Invalid album count: {len(invalid_albums_1) + len(invalid_albums_2) + len(invalid_albums_3)}")

# SPT.print_database()