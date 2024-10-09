from SpotifyTool import SpotifyTool
from AlbumDataTool import AlbumDataTool
from Album import Album

"""
Fix variable names... some too generic some too specific
"""

SPT = SpotifyTool()
ADT = AlbumDataTool()

r = SPT.get_album("The Beatles", "Revolver (Remastered)")
print(r)

# new_album = SPT.get_album("The Beatles", "Revolver")
# print(new_album)
# SPT.store_album(new_album)
# SPT.print_database()

# A = Album("jake's album","jake aldridge","www.fuck.com", "www.jake's-album.png", "12-01-1999")
# print(A)
# SPT.store_album(A)


# # Generate album data file from Billboard Top 200 dataset
# # ADT.write_album_data()
# # album_names_titles= ADT.read_album_data()

# SPT.print_tool_data()
# artist = "The Beatles"
# title = "Revolver (Remastered)"
# print(f"artist: {artist}")
# print(f"title: {title}")

# r = SPT.get_album_data(artist, title)
# if r[3] == title:
# 	print("success")
# else:
# 	print("failure")

# print(r)

# for data in album_names_titles:
# 	print(SPT.get_album_data(data[0], data[1]))

# SPT.initialize_album_data_storage()

# SPT.store_album_data("abc.com", "www.jakealdridge.com", "12-01-1999")