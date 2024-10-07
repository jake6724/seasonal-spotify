import pandas as pd
from collections import defaultdict

#TODO: Get rif of none at end of album_data.txt

class AlbumDataTool:
	def __init__(self) -> None:
		self.BILLBOARD_200_FILE = "billboard-200-current.csv"
		self.ALBUM_DATA_OUTPUT_FILE = "album_data.txt"

	def write_billboard_data(self) -> None:
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
		with open(self.ALBUM_DATA_OUTPUT_FILE, "r") as f:	 # TODO: Specify encoding
			for line in f:
				print(line.strip().split("/"))


# Runner
AT = AlbumDataTool()
AT.write_billboard_data()
r = AT.read_album_data()
print(r)