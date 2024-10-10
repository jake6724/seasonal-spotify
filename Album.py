# TODO: Release date formatting needs error handling

class Album():
	def __init__(self, title: str, artist: str, url: str, img_url: str, release_date: str) -> None:
		self.title: str = title
		self.artist: str = artist
		self.url: str = url
		self. img_url: str = img_url
		self.release_date: str = release_date
		print(self.release_date)

		self.process_release_date()

	def process_release_date(self) -> None:
		date_list = [int(date_value) for date_value in self.release_date.split("-")] # Create list of album release data. Cast each date value to int
		print(f"Date list: {date_list}")

		self.release_year = date_list[0]
		self.release_month = date_list[1]
		self.release_day = date_list[2]

	def __str__(self) -> None:
		# return f"Title: {self.title}, Artist: {self.artist}, URL: {self.url}, Image URL: {self.img_url}, Release date: {self.release_month}/{self.release_day}/{self.release_year}"
		return f"========================================================================================\n \
Title: {self.title}\n \
Artist: {self.artist}\n \
Release Data: {self.release_month}/{self.release_day}/{self.release_year}\n \
URL: {self.url}\n \
Image URL: {self.img_url}\n"