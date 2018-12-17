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
		self.result = 1
		self.my_score = 0

	def search(self):
		'''
		link_movie_name = re.sub(r"\s+", '+', self.name)
		link = "https://hk.search.yahoo.com/search?p="+link_movie_name+"+rotten+tomatoes+score"
		data = requests.get(link)
		soup = BeautifulSoup(data.text, "lxml")
		title = soup.find(class_ = "compTitle options-toggle")
		title = title.findAll(('a', {'class': 'ac-algo fz-l lh-20 tc d-ib va-mid', 'href': True}))
		title = str(title)
		title = title.split('"')
		self.tomatoter_link = title[5]
		'''

		find_movie_name = self.name
	
		'''if there are movies like XXX (full version), we just need XXX. So, stop reading when it read ('''
		find_movie_name = find_movie_name.split('(', 1)[0]
	
		'''change input to all lower case, remove punctuation, and replace whitespace by _'''
		find_movie_name = find_movie_name.lower()
		find_movie_name = re.sub(r"[,?!:']", '', find_movie_name)
		find_movie_name = re.sub(r"\s+", '_', find_movie_name)

		'''join it with link of rottentomatoes'''
		link = "https://www.rottentomatoes.com/m/"+find_movie_name+"_2018"
		data = requests.get(link)

		'''if no such movie, try _2018 or _2017, it is rottentomatoes rule'''
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
				if data.status_code == 200:
					self.tomatoter_link = link
				else:
					self.tomatoter_link = "not found"
					self.result = 0
	
	def rottemtomatoes_score(self):
		if self.tomatoter_link != "not found":
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
					self.my_score = int(self.tomatoter_score.strip('%'))
				else:
					self.tomatoter_score = "no tomatoter score"

				audience_score = soup.find(class_ = "audience-score meter")
				if audience_score:
					audience_score = audience_score.text
					audience_score= audience_score.strip(' \t\n\r')
					self.audience_score = audience_score[0:3]
				else:
					self.audience_score = "No audience score"
			else:
				self.result = 0
		else:
			self.result = 0


	def run(self):
		self.search()
		self.rottemtomatoes_score()



if __name__ == '__main__':
	user_input = input("please input a movie name: ")
	new_movie = MovieScore(user_input)
	new_movie.run()

