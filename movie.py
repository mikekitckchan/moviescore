from bs4 import BeautifulSoup
import requests
from rottentomatoes import MovieScore
import threading
import time
import cinemascore 

class NowMovieList(object):
	def __init__(self):
		print("Initiating.......")
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
			movie_dict = {}
			movie_dict['name'] = NewMovie.name
			movie_dict['tomatoter_score'] = NewMovie.tomatoter_score
			movie_dict['tomatoter_count'] = NewMovie.tomatoter_count
			movie_dict['production_company'] = NewMovie.production_company
			#movie_dict['review'] = NewMovie.review
			movie_dict['actors'] = NewMovie.actors
			movie_dict['director'] = NewMovie.director
			movie_dict['writers'] = NewMovie.writers
			movie_dict['genre'] = NewMovie.genre
			movie_dict['cinemascore']=cinemascore.getscore(movie_name)
			#movie_dict['cinemascore'] = newMovie.name
			self.movies_scores.append(movie_dict)

		

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

	def print_movies_scores(self):
		print("printing reuslt.......")
		for item in self.movies_scores:
			print(item)

	def run(self):
		self.get_movies_name()
		self.make_score_list()
		self.print_movies_scores()

if __name__ == '__main__':
	new_list = NowMovieList()
	new_list.run()

	
