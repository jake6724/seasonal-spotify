import json
import requests

"""
TODO: Add URL reponse checking / error handling
"""

class SpotifyTool: 
	def __init__(self):
		self.CLIENT_ID = ""
		self.CLIENT_SECRET = ""
		self.SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
		self.SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
		self.AUTH_TOKEN = ""
		self.CREDENTIALS_HEADER = {'Authorization': f'Bearer {self.AUTH_TOKEN}'}

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
		auth_token_dict = auth_token_request.json()
		access_token = auth_token_dict["access_token"]
		
		# Update global vars
		self.AUTH_TOKEN = access_token
		self.CREDENTIALS_HEADER = {'Authorization': f'Bearer {self.AUTH_TOKEN}'}


	def get_album_data(self, artist, album_name) -> tuple[str, str]:
		album_query = {
			'q': f'{artist} {album_name}',
			'type': 'album'
		}
		album_reponse = requests.get(self.SPOTIFY_SEARCH_URL, params=album_query, headers=self.CREDENTIALS_HEADER)

		album_data = album_reponse.json()	# Convert album json ovbject to dict

		album_url = (album_data["albums"]["items"][0]["external_urls"]["spotify"])
		album_img_url = (album_data["albums"]["items"][0]["images"][1]["url"])

		return (album_url, album_img_url)


	def download_img(self, image_url: str) -> None:
		image_data = requests.get(image_url).content
		with open("current_img", "wb") as f:
			f.write(image_data)


	def print_tool_data(self):
		print(f"CLIENT_ID: {self.CLIENT_ID}\nCLIENT_SECRET: {self.CLIENT_SECRET}\nSPOTIFY_TOKEN_URL: {self.SPOTIFY_TOKEN_URL}\nSPOTIFY_SEARCH_URL: {self.SPOTIFY_SEARCH_URL}\nAUTH_TOKEN: {self.AUTH_TOKEN}\nCREDENTIALS: {self.CREDENTIALS_HEADER}")

# runner 
# ST = SpotifyTool()
# ST.update_auth_token()

# # album_image_url = ST.get_album_image_url("https://open.spotify.com/album/4KKRAmQ0ksj32l7mrgLOcF")
# # print(album_image_url)

# ST.get_album_data("jamey johnson", "living for a song: a tribute to hank cochran")


# # ST.download_image(album_image_url)