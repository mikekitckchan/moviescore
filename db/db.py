import csv
from score.imdb import imdbMovie
import score.cinemascore as cinemascore
from score.rottentomatoes import MovieScore
import time
import shutil
from tempfile import NamedTemporaryFile
import os

fields = ['movie name', 'imdb name', 'year', 'description', 'trailer link', 'movie id', 'imdb score', 'rotten score', 'cinema score', 'user score']
timeout = 0

'''passing a row to make it to dictionary'''
def dictionarymaker(row):
	movie={}
	movie['moviename']=row['movie name']
	movie['year'] = row['year']
	movie['imdbname'] = row['imdb name']
	movie['descrip'] = row['description']
	movie ['trailerlink'] = row['trailer link'] 
	movie ['imdbscore'] = row['imdb score']
	movie ['rottenscore'] = row['rotten score']
	movie['cinemascore'] = row['cinema score']
	return movie

'''This function output relevant file to a list of dictionary'''
def readdb(dbfile, para = None):
	global fields
	output =[]
	if para == None:
		with open(dbfile, 'r') as csvfile:
			reader = csv.DictReader(csvfile, fieldnames=fields)
			for row in reader:
				if row['movie name']!= 'movie name':
					movie ={}
					movie = dictionarymaker(row)
					output.append(movie)
	else:
		with open(dbfile, 'r') as csvfile:
			reader = csv.DictReader(csvfile, fieldnames=fields)
			for row in reader:
				if para.lower() in row['movie name'].lower() or para.lower() in row['description'].lower():
					movie ={}
					movie=dictionarymaker(row)
					output.append(movie)
				else:
					pass
	return output

"""This function allows user to update one single movie into database"""
def updatedb(moviename, year):
	global fields
	filename = 'moviescore2.csv'
	tempfile = NamedTemporaryFile(mode='w', delete=False)
	with open(filename, 'r') as csvfile, tempfile:
		record_flag = 0
		reader = csv.DictReader(csvfile, fieldnames=fields)
		writer = csv.DictWriter(tempfile, fieldnames=fields)
		for row in reader:
			print('updating row', row['movie name'])
			if row['movie name'] == str(moviename) and row['year']==str(year):
				print('record exists')
				record_flag = 1
			print("moving "+row['movie name']+" to tempfile")
			writer.writerow(row)

		if record_flag == 0:
			writer.writerow(getmovieinfo(moviename, year))
	shutil.move(tempfile.name, filename)

"""This function take movie name and year of the movie, it would search the """
def getmovieinfo(moviename, year):
	movie ={}
	NewImdbMovie = imdbMovie(moviename, str(year))
	NewImdbMovie.run()
	NewRottenMovie = MovieScore(moviename)
	NewRottenMovie.run()
	movie['movie name']=moviename
	movie['year'] = str(year)
	movie['imdb name'] = NewImdbMovie.name
	movie['description'] = NewImdbMovie.description
	movie ['trailer link'] = NewImdbMovie.trailerlink
	movie ['movie id'] = NewImdbMovie.id
	movie ['imdb score'] = NewImdbMovie.score
	movie ['rotten score'] = NewRottenMovie.tomatoter_score
	movie['cinema score'] = str(cinemascore.getscore(moviename))
	movie['user score'] = "NA"
	return movie

def createdb(year):
	global fields

	readfilename = "./movielist/"+str(year)+".txt"
	writefilename = "./moviescorelist/moviescore"+str(year)+".csv"

	if os.path.isfile(writefilename):
		try:
			tempfile = NamedTemporaryFile(mode='w', delete=False)
			with open(readfilename, 'r') as txtfile:
				movies = txtfile.readlines()
				txtfile.close()
				with open('tempfile.csv', 'w', newline='') as tempfile:
					writer=csv.DictWriter(tempfile, fieldnames=fields)
					writer.writeheader()
					for items in movies:
						if len(items)>1:
							items = items.replace("\n", "")
							print("writing movie: "+items)
							movie = getmovieinfo(items, year)
							writer.writerow(movie)
							time.sleep(0.1)
						break
			shutil.move(tempfile.name, writefilename)
		except IOError:
			print("opps!")

	else:
		try:
			with open(readfilename, 'r') as txtfile:
				movies = txtfile.readlines()
				txtfile.close()
				with open(writefilename, 'w', newline='') as csvfile:
					writer = csv.DictWriter(csvfile, fieldnames=fields)
					writer.writeheader()
					for items in movies:
						print(items)
						print(len(items))
						if len(items)>1:
							items = items.replace("\n", "")
							print("writing movie: "+items)
							movie = getmovieinfo(items, year)
							writer.writerow(movie)
							time.sleep(0.1)
		except IOError:
			print("no movies availabe for such year")

if __name__ == '__main__':
	start_time = time.time()
	choice = input("input 0 if you want to create new database, 1 to updade existing db, 2 to read database")
	if choice == "0":
		for i in range(2007, 2008):
			createdb(i)
			print("successful update into database")
			end_time = time.time()
			print(end_time)
			period = (end_time - start_time)
			print("this db update takes: "+str(period)+" seconds")
	elif choice =="1":
		moviename=input("input a movie name")
		year=input("input the movie year")
		updatedb(moviename, year)
		print("successful update into database")
		end_time = time.time()
		print(end_time)
		period = (end_time - start_time)
		print("this db update takes: "+str(period)+" seconds")
	else:
		moviename = input("input a filename")
		result = readdb(moviename)
		print(result)

	


	


