from django.template import Context, loader
from django.http import HttpResponse
from bs4 import BeautifulSoup
from urllib import request
import re
import sys

#Get the first paragraph from a wikipedia entry and return it as an html string
def randomWiki():
	random_link = request.urlopen('http://en.wikipedia.org/wiki/Special:Random')
	if random_link.status == 200:
		link = random_link.geturl()
		soup = BeautifulSoup(random_link.read())
		p = soup.find('p')
		pString = str(p.text)
		return (link, pString)
	else:
		sys.exit("Sorry, there's a problem retrieving your random fact. [Error: %s]" % response.status_code)
		
#return a randomWiki() string and link if it contains verbs		
def verbCheck():
	randomObj = randomWiki()
	info = randomObj[1]
	verbs = re.search("\sis\s|\swas\s|\sare\s|\swere\s|occur|form", info)
	link = randomObj[0]
	while verbs is None:
		randomObj = randomWiki()
		info = randomObj[1]
		link = randomObj[0]
		verbs = re.search("\sis\s|\swas\s|\sare\s|\swere\s|occur|form", info)
	else:
		firstVerb = verbs.group()
		return (info, firstVerb, link)
		
#Split string into two parts that can be styled separately
def splitInfo():
	x = verbCheck()
	rawString = x[0]
	string = re.sub('\[\d+\]','',rawString) #strip out footnote link text
	splitPoint = x[1]
	link = x[2]
	split = re.split(splitPoint, string, 1)
	openString = split[0]
	endString = splitPoint + split[1]
	return (openString, endString, link)

def main(request):
	random_info = splitInfo()
	t = loader.get_template('main.html')
	c = Context({
		'info_start': random_info[0],
		'info_end': random_info[1],
		'link': random_info[2],
	})
	return HttpResponse(t.render(c))
