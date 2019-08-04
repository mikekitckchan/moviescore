from bs4 import BeautifulSoup
import requests
import re

def getmovielist(year):
	link = "https://www.wildaboutmovies.com/"+year+"_movies/" 
	data = requests.get(link)
	soup = BeautifulSoup(data.text, "html.parser")
	p = soup.find('article', {'class':'post-grid'})
	p = p.findAll('p')
	p=str(p)
	p = p.replace("<p>", "")
	p=p.replace("</p>","")
	p=p.replace(",", "\n")
	return p

if __name__ == '__main__':
	result=""
	for i in range (2017, 2020):
		result += getmovielist(str(i))
	text_file = open("movie.txt", "w")
	text_file.write(str(result))
	text_file.close()