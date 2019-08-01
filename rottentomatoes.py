from bs4 import BeautifulSoup
import requests
import re
import json

class MovieScore(object):
	def __init__(self, movie_name):
		self.name = movie_name
		self.tomatoter_name = ""
		self.tomatoter_score = ""
		self.tomatoter_count = ""
		self.tomatoter_link = ""
		self.production_company=""
		self.review=[]
		self.actors=[]
		self.director=[]
		self.writers=[]
		self.genre=[]
		self.result = 1
		self.my_score = 0
		

	def search(self):
		print("Searching: "+self.name)
		find_movie_name = self.name
	
		'''if there are movies like XXX (full version), we just need XXX. So, stop reading when it read ('''
		find_movie_name = find_movie_name.split('(', 1)[0]
	
		'''change input to all lower case, remove punctuation, and replace whitespace by _'''
		find_movie_name = find_movie_name.lower()
		find_movie_name = re.sub(r"[,?!:']", '', find_movie_name)
		find_movie_name = re.sub(r"\s+", '_', find_movie_name)

		'''join it with link of rottentomatoes'''
		link = "https://www.rottentomatoes.com/m/"+find_movie_name+"_2019"
		data = requests.get(link)

		'''if no such movie, try, _2019 _2018 or _2017, it is rottentomatoes rule'''
		if data.status_code == 200:
			self.tomatoter_link = link
		else:
			link = link.replace("_2019", "_2018")
			data = requests.get(link)
			if data.status_code == 200:
				self.tomatoter_link = link
			else:
				link = link.replace("_2018", "_2017")
				data = requests.get(link)
				if data.status_code == 200:
					self.tomatoter_link = link
				else:
					link = link.replace("_2017", "")
					data = requests.get(link)
					if data.status_code  == 200:
						self.tomatoter_link=link
					else:
						self.tomatoter_link = "not found"
						self.result = 0
		
	
	def rottemtomatoes_score(self):
		if self.tomatoter_link != "not found":
			data = requests.get(self.tomatoter_link)
			if data.status_code == 200:
				content = data.text
				soup = BeautifulSoup(content, "html.parser")
				p = soup.find('script', {'type':'application/ld+json'})
				p = json.loads(p.text)
				self.tomatoter_name = p["name"]
				self.tomatoter_score = p["aggregateRating"]["ratingValue"]
				self.tomatoter_count = p["aggregateRating"]["reviewCount"]
				
				try:
					self.production_company=p["productionCompany"]['name']
				except:
					pass
					
				for items in p['review']:
					self.review.append(items)
				for items in p['actors']:
					self.actors.append(items['name'])
				for items in p['director']:
					self.director.append(items['name'])
				for items in p['genre']:
					self.genre.append(items)

	def run(self):
		self.search()
		self.rottemtomatoes_score()
		
if __name__ == '__main__':
	user_input = input("please input a movie name: ")
	new_movie = MovieScore(user_input)
	new_movie.run()

