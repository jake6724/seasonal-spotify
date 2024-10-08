import json
import requests

"""
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


	def get_album_data(self, artist: str, album_name: str) -> tuple[str, str, str]:
		album_query = {
			'q': f'{artist} {album_name}',
			'type': 'album'
		}

		for attempt in range(self.MAX_RETRIES + 1):	# Allow 401 error to update token and retry specified number of times
			album_reponse = requests.get(self.SPOTIFY_SEARCH_URL, params=album_query, headers=self.CREDENTIALS_HEADER)

			if album_reponse.status_code == 200:
				try:
					album_data = album_reponse.json()	# Convert album json vbject to dict

					album_url = (album_data["albums"]["items"][0]["external_urls"]["spotify"])
					album_img_url = (album_data["albums"]["items"][0]["images"][1]["url"])
					album_release_date = (album_data["albums"]["items"][0]["release_date"])
					return (album_url, album_img_url, album_release_date)
				
				except Exception as e:
					print(e)
					return
				
			elif album_reponse.status_code == 401:
				self.update_auth_token()
		return	# Case that all attempts to access album data failed

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