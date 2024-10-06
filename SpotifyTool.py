import Constants as consts
import json
import requests
import subprocess


class SpotifyTool: 
	def __init__(self):
		test = 123
	
	def get_auth_token(self):
		payload = {
    			'grant_type': 'client_credentials',
    			'client_id': f'{consts.CLIENT_ID}',
    			'client_secret': f'{consts.CLIENT_SECRET}',
			}
	
		response = requests.post('https://accounts.spotify.com/api/token', data=payload)
		print(response.text)

# runner 

print(consts.CLIENT_ID)
print(consts.CLIENT_SECRET)

ST = SpotifyTool()

ST.get_auth_token()