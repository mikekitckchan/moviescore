from bs4 import BeautifulSoup
import requests
import re
import ast
from stringscore import liquidmetal
import json

class imdbMovie(object):
	def __init__(self, name):
		self.search_name=name
		self.id=""
		self.name = ""
		self.publishdate=""
		self.description=""
		self.trailerlink=""
		self.score=0

	def getid(self, moviename):
		moviename== re.sub(r"\s", '_', moviename)
		link = "https://v2.sg.media-imdb.com/suggestion/"+moviename[0]+"/"+moviename+".json" 
		print("getting id from "+link)
		data = requests.get(link)
		data = ast.literal_eval(data.text)
		data = data["d"]
		result =[]
		for items in data:
			score = liquidmetal.score(items["l"], moviename)
			print(score)
			if score >= 0.95:
				self.getinfo(items["id"])
				break
		

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
				self.score = 0
			try:
				self.publishdate = p["datePublished"]
			except:
				self.publishdate = "NA"
			try:
				self.description = p["description"]
			except:
				self.description = "NA"
			try:
				self.trailerlink = "https://www.imdb.com"+p["trailer"]["embedUrl"]
			except:
				self.trailerlink = "NA"

		else:
			self.score = -1

	def run(self):
		print(self.search_name)
		self.getid(self.search_name)


if __name__ == '__main__':
	moviename = input("Please enter your movie name: ")
	NewMovie = imdbMovie(moviename)
	NewMovie.run()
	print(NewMovie.name + " " + NewMovie.description + " " + NewMovie.trailerlink)

