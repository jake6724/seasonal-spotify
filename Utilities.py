import unicodedata

def remove_accents(text):
	 return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')