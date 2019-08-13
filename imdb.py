from bs4 import BeautifulSoup
import requests
import re
import ast
from stringscore import liquidmetal
import json
from ssl import SSLError
import requests.exceptions
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError

class imdbMovie(object):
	def __init__(self, name, year):
		self.search_name=name
		self.id="NA"
		self.name = "NA"
		self.year = year
		self.publishdate="NA"
		self.description="NA"
		self.trailerlink="NA"
		self.score=0

	def getid(self, moviename, year):
		moviename== re.sub(r"\s", '_', moviename)
		moviename = moviename.replace("\n", "")
		moviename = moviename.replace("?", "")
		moviename = moviename.replace("'","")
		link = "https://v2.sg.media-imdb.com/suggestion/"+moviename[0].lower()+"/"+moviename+".json"
		try: 
			data = requests.get(link)
			print("imdb response: "+str(data))
			data_string = data.text
		except (Timeout, SSLError, ReadTimeoutError, ConnectionError, ConnectionResetError):
			self.score = -1
			return
		except:
			self.score=-1
			return
		
		try:
			data = ast.literal_eval(data_string)
		except:
			self.score = -1
			return 
		try:
			data = data["d"]
		except:
			self.score = -1
			return
		result =[]
		for items in data:
			movieid = items["id"]
			try:
				if str(year) == str(items["y"]):
					self.getinfo(movieid)
					return
			except:
				pass
		self.score=-1

	def getinfo(self, movieid):
		link = "https://www.imdb.com/title/" + movieid + "/"
		print("getting movie info from " + link)
		data = requests.get(link)
		if data.status_code == 200:
			soup = BeautifulSoup(data.text, "html.parser")
			p = soup.find('script', {'type':'application/ld+json'})
			p = json.loads(p.text)
			self.id = movieid
			self.name = p["name"]
			try:
				self.score = p["aggregateRating"]["ratingValue"]
			except:
				pass
			try:
				self.publishdate = p["datePublished"]
			except:
				pass
			try:
				self.description = p["description"]
			except:
				pass
			try:
				self.trailerlink = "https://www.imdb.com"+p["trailer"]["embedUrl"]
			except:
				pass

		else:
			self.score = -1

	def run(self):
		self.getid(self.search_name, self.year)


if __name__ == '__main__':
	moviename = input("Please enter your movie name: ")
	NewMovie = imdbMovie(moviename, str(2002))
	NewMovie.run()
	print(NewMovie.name + " " + NewMovie.description + " " + NewMovie.trailerlink)

