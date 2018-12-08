from bs4 import BeautifulSoup
import requests
import re

class MovieScore(object):
	def __init__(self, movie_name):
		self.name = movie_name
		self.tomatoter_name = ""
		self.tomatoter_score = ""
		self.tomatoter_count = ""
		self.audience_score = ""
		self.tomatoter_link = ""

	def search(self):
		link_movie_name = re.sub(r"\s+", '+', self.name)
		link = "https://hk.search.yahoo.com/search?p="+link_movie_name+"+rotten+tomatoes+score"
		data = requests.get(link)
		soup = BeautifulSoup(data.text, "lxml")
		title = soup.find(class_ = "compTitle options-toggle")
		title = title.findAll(('a', {'class': 'ac-algo fz-l lh-20 tc d-ib va-mid', 'href': True}))
		title = str(title)
		title = title.split('"')
		self.tomatoter_link = title[5]
	
	def rottemtomatoes_score(self):
		data = requests.get(self.tomatoter_link)
		if data.status_code == 200:
			content = data.text
			soup = BeautifulSoup(content, "lxml")
			tomatoter = soup.find(class_ = "tomato-left")
			
			tomatoter_name = soup.find(('h1', {'class' : 'title hidden-xs no-trailer-title'}))
			if tomatoter_name:
				tomatoter_name = tomatoter_name.text
				tomatoter_name = tomatoter_name.strip(' \t\n\r')
				self.tomatoter_name = tomatoter_name
			else:
				self.tomatoter_name = "not found"
			
			tomatoter_count = tomatoter.find_all(class_ = "superPageFontColor")
			if tomatoter_count:
				tomatoter_count = tomatoter_count[3]
				tomatoter_count = tomatoter_count.text
				tomatoter_count = tomatoter_count [17:]
				self.tomatoter_count = tomatoter_count.strip(' \t\n\r')
			else:
				self.tomatoter_count = "no tomatoter reviews"
			
			tomatoter_score = tomatoter.find(class_ = "critic-score meter")
			if tomatoter_score:
				tomatoter_score = tomatoter_score.text
				self.tomatoter_score = tomatoter_score.strip(' \t\n\r')
			else:
				self.tomatoter_score = "no tomatoter score"

			audience_score = soup.find(class_ = "audience-score meter")
			if audience_score:
				audience_score = audience_score.text
				audience_score= audience_score.strip(' \t\n\r')
				self.audience_score = audience_score[0:3]
			else:
				self.audience_score = "No audience score"
			print("Newmovie name: " + self.name)
			print(" rotten name: " + self.tomatoter_name) 
			print(" rotten score: " + self.tomatoter_score + " no. of review: " + self.tomatoter_count)
			print("---")
		else:
			print(self.name + "not found")

	def run(self):
		self.search()
		self.rottemtomatoes_score()



if __name__ == '__main__':
	user_input = input("please input a movie name: ")
	new_movie = MovieScore(user_input)
	new_movie.run()

