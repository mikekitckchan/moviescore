from bs4 import BeautifulSoup
import requests
from rottentomatoes import MovieScore

movies = []
movies_scores = []
data = requests.get("https://nowplayer.now.com/ondemand/seeall?filterType=appPlayable&nodeId=C201008200000129")
content = data.text
soup = BeautifulSoup(content, "lxml")
titles = soup.find_all('p', attrs={'class' : 'title'})

for title in titles:
	movies.append(title.text)

for item in movies:
	print("reading "+item)
	NewMovie = MovieScore(item)
	NewMovie.run()
	
