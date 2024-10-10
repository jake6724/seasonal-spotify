import pandas as pd
import csv
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
		self.INPUT_FILE = "billboard-200-current.csv"
		self.OUTPUT_FILE = "album_data.txt"

	def process_album_data(self) -> list[list[str, str, str]]:
		"""Process csv file, return list of album info. Each 'album info' is a list of [artist, album title, release date]"""
		seen = set()
		album_list = []

		with open(self.INPUT_FILE, "r") as input, open(self.OUTPUT_FILE, "w") as output:
			data = csv.reader(input, delimiter=',')
			for line in data:
				album_info = [line[3], line[2], line[0]] # Artist, album title, release date

				album_id = f"{album_info[0]} {album_info[1]}"	# Only store each album one time
				if album_id not in seen:
					seen.add(album_id)
					album_list.append(album_info)

		return album_list