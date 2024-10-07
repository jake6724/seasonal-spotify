]]
import json
import requests
from bs4 import BeautifulSoup as bs

"""
TODO: Add URL reponse checking / error handling
"""

class SpotifyTool: 
	def __init__(self):
		self.CLIENT_ID = "9a7802fd1a194ad884d73abf47de35f2"
		self.CLIENT_SECRET = "aff44ac1c3f341d39b945a2875a5ad07"
		self.SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
		self.AUTH_TOKEN = ""

	def update_auth_token(self) -> None:
		"""Update the value of AUTH_TOKEN in Constants"""	
		credentials_payload = {	
    			'grant_type': 'client_credentials',
    			'client_id': f'{self.CLIENT_ID}',
    			'client_secret': f'{self.CLIENT_SECRET}',
			}
	
		auth_token_json = requests.post('https://accounts.spotify.com/api/token', data=credentials_payload)
		auth_token_dict = json.loads(auth_token_json.text)	
		access_token = auth_token_dict["access_token"]

		self.AUTH_TOKEN = access_token

	def get_album_image_url(self, album_url: str) -> str:
		"""Return the URL of the image for the specified album"""
		credentials = {'Authorization': f'Bearer  {self.AUTH_TOKEN}',}
		album_html = requests.get(album_url, headers=credentials)

		parsed_album_html = bs(album_html.text, 'html.parser')
		# Find the <meta> tag where property equals "og:image"
		meta_tag = parsed_album_html.find('meta', {'property': 'og:image'})

		# Extract the 'content' attribute from the meta tag
		if meta_tag:
			image_url = meta_tag.get('content')
		else:
			print('Meta tag with property "og:image" not found.')

		return image_url
		
	def download_image(self, image_url: str) -> None:
		image_data = requests.get(image_url).content
		with open("test.png", "wb") as f:
			f.write(image_data)


# runner 
ST = SpotifyTool()
ST.update_auth_token()

album_image_url = ST.get_album_image_url("https://open.spotify.com/album/4KKRAmQ0ksj32l7mrgLOcF")
print(album_image_url)

ST.download_image(album_image_url)