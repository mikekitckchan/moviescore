from bs4 import BeautifulSoup
import requests
import re
import json
import base64

def get_moviescore(moviename):
	moviename = moviename.encode(encoding="utf-8")
	moviename = base64.b64encode(moviename)
	moviename = moviename.decode(encoding="utf-8")
	print(str(moviename))
	link = "https://www.cinemascore.com/publicsearch/ajax/title/"+str(moviename)
	print(link)
	data = requests.get(link)
	print(data.text)

if __name__ == '__main__':
	moviename = input("Please enter your movie name: ")
	get_moviescore(moviename)
