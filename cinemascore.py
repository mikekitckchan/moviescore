from bs4 import BeautifulSoup
import requests
import re
import base64

def getscore(moviename):
	moviename = moviename.encode(encoding="utf-8")
	moviename = base64.b64encode(moviename)
	moviename = moviename.decode(encoding="utf-8")
	link = "https://www.cinemascore.com/publicsearch/ajax/title/"+str(moviename)
	data = requests.get(link)
	soup = BeautifulSoup(data.text, "html.parser")
	try:
		score = soup.find('img')['alt']
	except:
		score = -1
	return score

if __name__ == '__main__':
	moviename = input("Please enter your movie name: ")
	getscore(moviename)
