import json
import requests
import traceback
import Utilities
from Album import Album

"""
TODO: Convert print statements to a log
TODO: Add type hinting to func params
TODO: Finish all Docstrings
"""

class SpotifyTool: 
	def __init__(self) -> None:
		self.CLIENT_ID = ""
		self.CLIENT_SECRET = ""
		self.SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
		self.SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
		self.AUTH_TOKEN = ""
		self.CREDENTIALS_HEADER = {'Authorization': f'Bearer {self.AUTH_TOKEN}'}
		self.MAX_RETRIES = 1
		self.REQUEST_COUNT = 10
		self.read_credentials()
		self.update_auth_token()

		self.database = {}
		self.initialize_album_database()

		# Return codes
		self.SUCCESS = 0
		self.AUTH_FAILED = 1
		self.NO_QUERY_ITEMS_MATCH = 2
		self.ERROR_PROCESSING_ALBUM_ITEM = 3

	def read_credentials(self) -> None:
		# Read client creds from local file
		with open("client_creds", "r") as client_creds:
			creds = client_creds.readlines()
			self.CLIENT_ID = creds[0].strip()
			self.CLIENT_SECRET = creds[1].strip()
	
	def update_auth_token(self) -> None:
		"""Update the value of AUTH_TOKEN in Constants"""	

		credentials_payload = {
    			'grant_type': 'client_credentials',
    			'client_id': f'{self.CLIENT_ID}',
    			'client_secret': f'{self.CLIENT_SECRET}'
			}
	
		auth_token_request = requests.post(self.SPOTIFY_TOKEN_URL, data=credentials_payload)

		if auth_token_request.status_code == 200:
			try:
				auth_token_dict = auth_token_request.json()
				access_token = auth_token_dict["access_token"]
			except Exception as e:
				print(e)
				return
		elif auth_token_request.status_code == 400:
			print(auth_token_request.text)
			print("Check that client credentials in 'client_creds' are correct")
			return
		else:
			print(auth_token_request.text)
			return

		# Update global vars
		self.AUTH_TOKEN = access_token
		self.CREDENTIALS_HEADER = {'Authorization': f'Bearer {self.AUTH_TOKEN}'}

	def initialize_album_database(self) -> None:
		"""Create dict with year-month:[] structure. Used to store album image urls."""
		months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
		for year in range(1958, 2025):
			for month in months:
				key = f"{year}-{month}"
				self.database[key] = [] 

	def get_album(self, query_artist: str, query_title: str) -> tuple[Album, int]:
		"""Get album by artist and title with Spotify API.\nReturn: Album obj. and return code."""
		query_artist = query_artist.lower()
		query_title = query_title.lower()

		album_query = {
			'q': f'{query_artist} {query_title}',
			'type': 'album',
			'limit': f'{self.REQUEST_COUNT}'
		}		

		for query in range(self.MAX_RETRIES + 1):	# Reset auth_token if query fails specified number of times
			album_reponse = requests.get(self.SPOTIFY_SEARCH_URL, params=album_query, headers=self.CREDENTIALS_HEADER)

			if album_reponse.status_code == 401:
				self.update_auth_token()
				continue

			elif album_reponse.status_code == 200:
				try:
					for i in range(self.REQUEST_COUNT): 	# Try all items returned by request
						album_data = album_reponse.json()	

						album_release_date_precision = (album_data["albums"]["items"][0]["release_date_precision"]).strip() 
						if album_release_date_precision != "day": # This could be month, with extra error handling
							continue

						album_title = (album_data["albums"]["items"][i]["name"]).strip().lower()
						album_artist = (album_data["albums"]["items"][i]["artists"][0]["name"]).strip().lower() # TODO: This will only grab the first artist listed
						album_url = (album_data["albums"]["items"][i]["external_urls"]["spotify"]).strip()
						album_img_url = (album_data["albums"]["items"][i]["images"][1]["url"]).strip()
						album_release_date = (album_data["albums"]["items"][i]["release_date"]).strip()
						new_album = Album(album_title, album_artist, album_url, album_img_url, album_release_date)

						self.debug_album(i, new_album)

						if self.validate_album(query_artist, query_title, new_album):
							print(new_album)
							self.store_album(new_album)
							return (new_album, self.SUCCESS)
						
					return (None, self.NO_QUERY_ITEMS_MATCH)
				
				except Exception:
					print(traceback.format_exc())
					return (None, self.ERROR_PROCESSING_ALBUM_ITEM)

		return (None, self.AUTH_FAILED)
	
	def validate_album(self, query_artist: str, search_album_title: str, Album: Album) -> bool:
		"""
		Check whether the meta-data in Album obj. matches the original query parameters\n
		This is intended to check if get_album() returned the correct album, since the spotify API will return options even if it cannot find an exact match
		to the search query. This method is not full-proof.
		""" 

		return True if (Album.artist == query_artist) and (Album.title == search_album_title) else False

	def store_album(self, album: Album) -> None:
		key = f"{album.release_year}-{album.release_month_name}"
		self.database[key].append(album.img_url)

	# def write_database

	def download_img(self, image_url: str) -> None:
		try:
			img_download_response = requests.get(image_url)
		except Exception as e:
			print(e)
			return 

		if img_download_response == 200:
			img_download_content = img_download_response.content
			with open("current_img", "wb") as f:
				f.write(img_download_content)
		else:
			print("Non 200 status code recieved during image download")

	def debug_album(self, index: int, new_album: Album) -> None: # Write to a file for debugging
		with open(f"./debug/album_items.txt", "a") as f: 
			f.write(f"Item {index}===============================================================================================\n")
			f.write(f"album_title: {new_album.title}\n")
			f.write(f"album_artist: {new_album.artist}\n")
			f.write(f"album_artist: {new_album.url}\n")
			f.write(f"album_artist: {new_album.img_url}\n")
			f.write(f"album_artist: {new_album.release_date}\n")

	def print_tool_data(self) -> None:
		print(f"CLIENT_ID: {self.CLIENT_ID}\nCLIENT_SECRET: {self.CLIENT_SECRET}\nSPOTIFY_TOKEN_URL: {self.SPOTIFY_TOKEN_URL}\nSPOTIFY_SEARCH_URL: {self.SPOTIFY_SEARCH_URL}\nAUTH_TOKEN: {self.AUTH_TOKEN}\nCREDENTIALS: {self.CREDENTIALS_HEADER}")

	def print_database(self) -> None:
		# TODO: Output too large to be useful. Maybe write to a file in a nicely formatted way?
		for key in self.database.keys():
			print(f"{key}: {self.database[key]}")