from SpotifyTool import SpotifyTool
from AlbumDataTool import AlbumDataTool
from Album import Album

SPT = SpotifyTool()
ADT = AlbumDataTool()
invalid_albums_1 = []
invalid_albums_2 = []
invalid_albums_3 = []
invalid_albums_4 = []

# # Generate album list from Billboard Top 200 csv
album_list = ADT.process_album_data()

# # Iterate through album list, search for each album with Spotify API
with open("run1.log") as rl:
	size = len(album_list) - 1
	for i, album_data in enumerate(album_list):
		result = SPT.get_album(album_data[0], album_data[1])
		if result[1] == 0:
			rl.write(f"({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]} --- [SUCCEEDED][0]")
			print(f"({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]} --- [SUCCEEDED][0]")
		elif result[1] == 1:
			rl.write("({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]} --- [FAILED][1]")
			print(f"({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]} --- [FAILED][1]")
			invalid_albums_1.append(f"{album_data[0]}, {album_data[1]}, return code: {result[1]}")
		elif result[1] == 2:
			rl.write(f"({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]} --- [FAILED][2]")
			print(f"({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]} --- [FAILED][2]")
			invalid_albums_2.append(f"{album_data[0]}, {album_data[1]}, return code: {result[1]}")
		elif result[1] == 3:
			rl.write(f"({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]} --- [FAILED][3]")
			print(f"({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]} --- [FAILED][3]")
			invalid_albums_3.append(f"{album_data[0]}, {album_data[1]}, return code: {result[1]}")
		elif result[1] == 4:
			rl.write(f"({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]} --- [FAILED][4]")
			print(f"({i}/{size}) Artist: {album_data[0]}, Title: {album_data[1]} --- [FAILED][4]")
			invalid_albums_4.append(f"{album_data[0]}, {album_data[1]}, return code: {result[1]}")
			break

print(f"Invalid albums 1: {invalid_albums_1}")
print(f"Invalid albums 2: {invalid_albums_2}")
print(f"Invalid albums 3: {invalid_albums_3}")
print(f"Invalid albums 4: {invalid_albums_4}")
print(f"Invalid album count: {len(invalid_albums_1) + len(invalid_albums_2) + len(invalid_albums_3)}")

# SPT.print_database()