import Constants as consts
import json
import requests
import subprocess


class SpotifyTool: 
	def __init__(self):
		test = 123
	
	def get_auth_token(self):
		auth_data = {
			'grant_type': 'client_credentials',
			'client_id': consts.CLIENT_ID,
			'client_secret': consts.CLIENT_SECRET
		}

		# print(auth_data)

		auth_data_json = json.dumps(auth_data)

		print(auth_data_json)
		


		pl = {
    			'grant_type': 'client_credentials',
    			'client_id': f'{consts.CLIENT_ID}',
    			'client_secret': f'{consts.CLIENT_SECRET}',
			}
		print(pl)
			
		# response = requests.post('https://accounts.spotify.com/api/token', data=pl)
		# print(response.text)

# runner 

print(consts.CLIENT_ID)
print(consts.CLIENT_SECRET)

ST = SpotifyTool()

ST.get_auth_token()