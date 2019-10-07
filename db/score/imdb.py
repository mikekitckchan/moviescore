from bs4 import BeautifulSoup
import requests
import re
import ast
import json
from ssl import SSLError
import requests.exceptions
from requests.exceptions import Timeout, ConnectionError, Timeout
from urllib3.exceptions import ReadTimeoutError
from difflib import SequenceMatcher

class imdbMovie(object):
	def __init__(self, name, year):
		self.search_name=name
		self.id="NA"
		self.name = "NA"
		self.year = year
		self.publishdate="NA"
		self.description="NA"
		self.trailerlink="NA"
		self.score="NA"

	def getid(self, moviename, year):
		moviename== re.sub(r"\s", '_', moviename)
		moviename = moviename.replace("\n", "")
		moviename = moviename.replace("?", "")
		moviename = moviename.replace("'","")
		link = "https://v2.sg.media-imdb.com/suggestion/"+moviename[0].lower()+"/"+moviename+".json"

		
		try: 
			data = requests.get(link, timeout=10)
			data_string = data.text
		except (Timeout, SSLError, ReadTimeoutError, ConnectionError, ConnectionResetError, Timeout):
			self.score = "NA"
			return
		except:
			self.score="NA"
			return
		
		try:
			data = ast.literal_eval(data_string)
		except:
			self.score = "NA"
			return 
		try:
			data = data["d"]
		except:
			self.score = "NA"
			return
		result =[]
		flag1=0
		flag2=0
		result1=0
		result2=0

		for items in data:
			movieid = items["id"]
			try:
				if abs(int(year)- int(items["y"]))<3 and flag2 ==0:
					flag2=1
					result2=movieid
			except:
				pass
			try:
				if SequenceMatcher(None, items["l"], moviename).ratio()>0.95 and abs(int(year)-int(items["y"]))<3 and flag1==0:
					result1=movieid
					flag1=1
			except:
				pass
				
		if result1!=0:
			self.getinfo(str(result1))
			
			return
		else:
			self.getinfo(str(result2))
		
			return
		self.score="NA"

	def getinfo(self, movieid):
		link = "https://www.imdb.com/title/" + movieid + "/"
		#print("getting movie info from " + link)
		data = requests.get(link)
		print(data.status_code)
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
			self.score = "NA"

	def run(self):
		self.getid(self.search_name, self.year)


if __name__ == '__main__':
	moviename = input("Please enter your movie name: ")
	NewMovie = imdbMovie(moviename, str(2007))
	NewMovie.run()
	print(NewMovie.name + " " + NewMovie.description + " " + NewMovie.trailerlink)

