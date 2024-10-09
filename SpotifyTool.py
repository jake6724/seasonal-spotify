import json
import requests
import traceback
from collections import defaultdict
from Album import Album

"""
TODO: Figure out what to do about album names with like remasted and stuff in them

TODO: Add URL reponse checking / error handling
TODO: Convert print statements to an error log ? 
TODO: Add type hinting to func params
TODO: Finish all Docstrings
"""

class SpotifyTool: 
	def __init__(self):
		self.CLIENT_ID = ""
		self.CLIENT_SECRET = ""
		self.SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
		self.SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
		self.AUTH_TOKEN = ""
		self.CREDENTIALS_HEADER = {'Authorization': f'Bearer {self.AUTH_TOKEN}'}
		self.MAX_RETRIES = 1
		self.read_credentials()
		self.update_auth_token()

		self.album_database = {}
		self.initialize_album_database()

	def read_credentials(self):
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

	def initialize_album_database(self):
		"""Create database structure:\n
		   self.album_database = {1999: {1: {1:[], 2:[], 3:[], etc.}, 2:{1:[], 2:[], 3:[], etc.}, etc.}, 2000: {1: {1:[], 2:[], 3:[], etc.}, 2:{1:[], 2:[], 3:[], etc.}, etc.}}}\n
		   Database can be accessed SpotifyTool.album_database[year][month][day][index]. 
		   [day] points to a list which contains all albums released that day, unsorted.

		"""
		for year in range(1958, 2022):
			self.album_database[year] = {}
			for month in range(1, 13):
				self.album_database[year][month] = {}
				for day in range(1, 31):
					self.album_database[year][month][day] = []

	def print_database(self):
		# TODO: Output too large to be useful. Maybe write to a file in a nicely formatted way?
		for year in self.album_database:
			print(f"{year}: {self.album_database[year]}")

	def get_album(self, artist: str, album_title: str) -> Album:
		"""
		Get album by artist and title with Spotify API.\n
		Return: new Album obj.  
		"""
		album_query = {
			'q': f'{artist} {album_title}',
			'type': 'album',
			'limit': 1
		}

		for attempt in range(self.MAX_RETRIES + 1):	# Allow 401 error to update token and retry specified number of times
			album_reponse = requests.get(self.SPOTIFY_SEARCH_URL, params=album_query, headers=self.CREDENTIALS_HEADER)

			if album_reponse.status_code == 200:
				try:
					album_data = album_reponse.json()	# Convert album json object to dict

					# TODO: Is there a better way to search for all of this? Maybe JMEPath package
					album_title = (album_data["albums"]["items"][0]["name"]).strip()
					album_artist = (album_data["albums"]["items"][0]["artists"][0]["name"]).strip() # TODO: This will only grab the first artist listed
					album_url = (album_data["albums"]["items"][0]["external_urls"]["spotify"]).strip() 
					album_img_url = (album_data["albums"]["items"][0]["images"][1]["url"]).strip() 
					album_release_date = (album_data["albums"]["items"][0]["release_date"]).strip() 
					new_album = Album(album_title, album_artist, album_url, album_img_url, album_release_date)

					# Try to validate if the album accessed is the album intended by the query above
					return new_album if self.validate_album(artist, album_title, new_album) else None
				
				except Exception:
					print(traceback.format_exc())
					return
				
			elif album_reponse.status_code == 401:
				self.update_auth_token()
		return	# Case that all attempts to access album data failed
	
	def validate_album(self, search_artist: str, search_album_title: str, Album: Album) -> bool:
		"""
		Check whether the meta-data in Album obj. matches the original search parameter\n
		This is intended to check if get_album() returned the correct album, since the spotify API will return options even if it cannot find an exact match
		to the search query. This method is likely not full-proof...
		"""
		# print(f"Comparing {Album.artist} to {search_artist}")
		# print(f"Comparing {Album.title} to {search_album_title}") 
		return True if (Album.artist == search_artist) and (Album.title == search_album_title) else False

	def store_album(self, album: Album) -> None:
		self.album_database[album.release_year][album.release_month][album.release_day].append(album.img_url)	# Store the album img url at year -> month -> day [img_url]

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

	def print_tool_data(self):
		print(f"CLIENT_ID: {self.CLIENT_ID}\nCLIENT_SECRET: {self.CLIENT_SECRET}\nSPOTIFY_TOKEN_URL: {self.SPOTIFY_TOKEN_URL}\nSPOTIFY_SEARCH_URL: {self.SPOTIFY_SEARCH_URL}\nAUTH_TOKEN: {self.AUTH_TOKEN}\nCREDENTIALS: {self.CREDENTIALS_HEADER}")