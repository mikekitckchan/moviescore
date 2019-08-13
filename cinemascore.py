from bs4 import BeautifulSoup
import requests
import re
import base64
from ssl import SSLError
import requests.exceptions
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError

def getscore(moviename):
	score = -1
	moviename = moviename.encode(encoding="utf-8")
	moviename = base64.b64encode(moviename)
	moviename = moviename.decode(encoding="utf-8")
	link = "https://www.cinemascore.com/publicsearch/ajax/title/"+str(moviename)
	try:
		data = requests.get(link)
		print("moviescore response: "+str(data))
		soup = BeautifulSoup(data.text, "html.parser")
	except (Timeout, SSLError, ReadTimeoutError, ConnectionError, ConnectionResetError):
		return score
	except:
		return score
	
	try:
		score = soup.find('img')['alt']
	except:
		return score
	return score

if __name__ == '__main__':
	moviename = input("Please enter your movie name: ")
	print(getscore(moviename))
