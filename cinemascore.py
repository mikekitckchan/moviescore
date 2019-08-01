from bs4 import BeautifulSoup
import requests
import re
import json
import base64

def getscore(moviename):
	moviename = moviename.encode(encoding="utf-8")
	moviename = base64.b64encode(moviename)
	moviename = moviename.decode(encoding="utf-8")
	print(str(moviename))
	link = "https://www.cinemascore.com/publicsearch/ajax/title/"+str(moviename)
	print(link)
	data = requests.get(link)
	soup = BeautifulSoup(data.text, "html.parser")
	try:
		score = soup.find('img')['alt']
	except:
		pass
	return score

if __name__ == '__main__':
	moviename = input("Please enter your movie name: ")
	getscore(moviename)
