import csv

"""
TODO: 'various artists' is a very common artist... is this an issue?
"""

class AlbumDataTool:
	def __init__(self) -> None:
		self.INPUT_FILE = "billboard-200-current.csv"
		self.OUTPUT_FILE = "album_data.txt"

	def process_album_data(self) -> list[list[str, str, str]]:
		"""Process csv file, return list of sublists of format [artist, album title, release date]"""
		seen = set()
		album_list = []

		with open(self.INPUT_FILE, "r") as input:
			data = csv.reader(input, delimiter=',')
			for line in data:
				album_info = [line[3], line[2], line[0]] 		# Artist, album title, release date

				album_id = f"{album_info[0]} {album_info[1]}"	# Only store each album one time
				if album_id not in seen:
					seen.add(album_id)
					album_list.append(album_info)

		return album_list