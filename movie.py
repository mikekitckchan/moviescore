from bs4 import BeautifulSoup
import requests
from rottentomatoes import MovieScore
import threading
import time

class NowMovieList(object):
	def __init__(self):
		print("Instantiating........")
		self.link = "https://nowtv.now.com/now-select/movie?lang=en"
		self.movies = []
		self.movies_scores = []

	def get_movies_name(self):
		print("getting Now Movie List.......")
		data = requests.get(self.link)
		content = data.text
		soup = BeautifulSoup(content, "html.parser")
		titles = soup.find_all('div', attrs={'class' : 'program_title'})
		for title in titles:
			self.movies.append(title.text)

	def get_movies_scores(self, movie_name):
		NewMovie = MovieScore(movie_name)
		NewMovie.run()
		if NewMovie.result == 1:
			self.movies_scores.append(NewMovie)
		

	def make_score_list(self):
		print("getting movie score.............")
		threads =[]
		for item in self.movies:
			t = threading.Thread(target=self.get_movies_scores, args=[item,])
			threads.append(t)
			t.start()
			time.sleep(1)

		main_thread = threading.currentThread()
		for t in threading.enumerate():
			if t is main_thread:
				continue
			t.join()

		self.movies_scores.sort(key=lambda x: x.my_score, reverse=True)


	def print_movies_scores(self):
		print("printing reuslt.......")
		for item in self.movies_scores:
			print("name: "+str(item.name))
			print("tomatoter score: "+str(item.tomatoter_score))
			print("number of reviews: "+str(item.tomatoter_count))
			print("----------------")

	def run(self):
		self.get_movies_name()
		self.make_score_list()
		self.print_movies_scores()

if __name__ == '__main__':
	new_list = NowMovieList()
	new_list.run()

	
