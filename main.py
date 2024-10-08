from SpotifyTool import SpotifyTool
from AlbumDataTool import AlbumDataTool

"""
Fix variable names... some too generic some too specific
"""

SPT = SpotifyTool()
ADT = AlbumDataTool()

# Generate album data file from Billboard Top 200 dataset
ADT.write_album_data()
album_data = ADT.read_album_data()

SPT.update_auth_token()
SPT.print_tool_data()

for data in album_data:
	print(SPT.get_album_data(data[0], data[1]))

