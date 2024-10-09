import pandas as pd
from collections import defaultdict

"""
TODO: Need to store release date with url and img
TODO: Add type hinting to func params

TODO: Get rid of none at end of album_data.txt
TODO: 'various artists' is a very common artist... is this an issue?
TODO: Add type hinting to func params
"""

class AlbumDataTool:
	def __init__(self) -> None:
		self.BILLBOARD_200_FILE = "billboard-200-current.csv"
		self.ALBUM_DATA_OUTPUT_FILE = "album_data.txt"

	def write_album_data(self) -> None:
		"""Process the data from billboard-200-current.csv and write it to a txt file"""
		ALBUM_DATA_FILE = "album_data.txt"
		BILLBOARD_200_FILE = "billboard-200-current.csv"

		billboard_200_dataframe = pd.read_csv(BILLBOARD_200_FILE)
		albums = defaultdict(int)

		for row in billboard_200_dataframe.iterrows():
			album_performer = str(row[1]['performer'])
			album_title = str(row[1]['title'])
			album_info = (album_performer + "/" + album_title).lower()
			
			if albums[album_info] == 0:
				albums[album_info] = 1

		with open(ALBUM_DATA_FILE, "w") as album_data:
			for key in sorted(albums.keys()):
				album_data.write(f"{key}\n")
	
	def read_album_data(self) -> list[list[str]]:
		"""
		Return a list of album data that was written to the album data file. 
		Album data is stored as a sublist [album_performer, album_title]
		"""
		album_data_list = []
	

		with open(self.ALBUM_DATA_OUTPUT_FILE, "r") as album_data:	 # TODO: Specify encoding
			for line in album_data:
				album_data_list.append(line.strip().split("/"))
		return album_data_list