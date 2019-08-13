import csv
from imdb import imdbMovie
import cinemascore
from rottentomatoes import MovieScore
import time

def writedb(year):
	fields = ['movie name', 'imdb name', 'year', 'description', 'trailer link', 'movie id', 'imdb score', 'rotten score', 'cinema score', 'user score']

	filename = str(year) + ".txt"

	try:
		with open(filename, 'r') as txtfile:
			movies = txtfile.readlines()
			txtfile.close()
	except:
		print("no movies availabe for such year")

	with open('moviescore.csv', 'w', newline='') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fields)
		writer.writeheader()
		for items in movies:
			items = items.replace("\n", "")
			print("Writing "+items)
			movie ={}
			NewImdbMovie = imdbMovie(items, str(year))
			NewImdbMovie.run()
			NewRottenMovie = MovieScore(items)
			NewRottenMovie.run()
			movie['movie name'] = items
			movie['imdb name'] = NewImdbMovie.name
			movie['year'] = year
			movie['description'] = NewImdbMovie.description
			movie ['trailer link'] = NewImdbMovie.trailerlink
			movie ['movie id'] = NewImdbMovie.id
			movie ['imdb score'] = NewImdbMovie.score
			movie ['rotten score'] = NewRottenMovie.tomatoter_score
			movie['cinema score'] = str(cinemascore.getscore(items))
			movie['user score'] = "NA"
			writer.writerow(movie)
			time.sleep(3)

if __name__ == '__main__':
	start_time = time.time()
	movie_year = input("which year you want to write to the database?")
	writedb(movie_year)
	print("successful write into database")
	end_time = time.time()
	period = end_time - start_time
	print("this db update takes: "+str(period))


	


