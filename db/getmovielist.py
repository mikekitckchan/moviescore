from bs4 import BeautifulSoup
import requests
import re
import datetime

def getmovielist(year):
	link = "https://www.wildaboutmovies.com/"+year+"_movies/" 
	data = requests.get(link)
	soup = BeautifulSoup(data.text, "html.parser")
	p = soup.find('article', {'class':'post-grid'})
	p = p.findAll('a')
	movies = ""
	for items in p:
		movies += str(items.find('p')) + "\n"
	movies = movies.replace("<p>", "")
	movies = movies.replace("</p>", "")
	return movies

if __name__ == '__main__':
	result=""
	now = datetime.datetime.now()
	currentyear = str(now.year)
	result = getmovielist(currentyear)
	text_file = open("./movielist/"+currentyear+".txt", "w")
	text_file.write(str(result))
	text_file.close()