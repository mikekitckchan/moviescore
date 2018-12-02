from bs4 import BeautifulSoup
import requests
import re


def GetMovieScore(user_input):
	original_input = user_input
	
	'''if there are movies like XXX (full version), we just need XXX. So, stop reading when it read ('''
	user_input = user_input.split('(', 1)[0]
	
	'''change input to all lower case, remove punctuation, and replace whitespace by _'''
	user_input = user_input.lower()
	user_input = re.sub(r"[,?!:']", '', user_input)
	user_input = re.sub(r"\s+", '_', user_input)
	
	'''join it with link of rottentomatoes'''
	link = "https://www.rottentomatoes.com/m/"+user_input+"_2018"
	data = requests.get(link)

	'''if no such movie, try _2018 or _2017, it is rottentomatoes rule'''
	if data.status_code != 200:
		link = link.replace("_2018", "_2017")
		data = requests.get(link)
		if data.status_code != 200:
			link = link.replace("_2017", "")
			data = requests.get(link)

	'''if exists, find the score, number of comments etc from the page'''
	if data.status_code == 200:
		content = data.text
		soup = BeautifulSoup(content, "lxml")
		tomatoter = soup.find(class_ = "tomato-left")

		'''find the number of tomatoter reviews'''
		tomatoter_count = tomatoter.find_all(class_ = "superPageFontColor")
		if tomatoter_count:
			tomatoter_count = tomatoter_count[3]
			tomatoter_count = tomatoter_count.text
			tomatoter_count = tomatoter_count [17:]
			tomatoter_count = tomatoter_count.strip(' \t\n\r')
		else:
			tomatoter_count = "no tomatoter reviews"

		'''find the tomatoter score'''
		tomatoter_score = tomatoter.find(class_ = "critic-score meter")
		if tomatoter_score:
			tomatoter_score = tomatoter_score.text
			tomatoter_score = tomatoter_score.strip(' \t\n\r')
		else:
			tomatoter_score = "no tomatoter score"

		'''find the audience score'''
		audience_score = soup.find(class_ = "audience-score meter")
		if audience_score:
			audience_score = audience_score.text
			audience_score= audience_score.strip(' \t\n\r')
			audience_score = audience_score[0:3]
		else:
			audience_score = "No audience score"

		result = {"movie name": original_input, "result": {"tomatoter_score":tomatoter_score, "number of tomatoter reviews": tomatoter_count, "audience_score": audience_score}}

	else:
		result = {"movie name": original_input, "result": {"not found"}}

	return result

if __name__ == '__main__':
	user_input = input("Please input a moview name: ")
	print(GetMovieScore(user_input))

