from bs4 import BeautifulSoup
import requests
import re
import json

link = "https://www.rottentomatoes.com/m/spider_man_far_from_home/"
data = requests.get(link)
content = data.text
soup = BeautifulSoup(content, "html.parser")
p = json.loads(soup.find('script', {'type':'application/ld+json'}).text)
print(p)