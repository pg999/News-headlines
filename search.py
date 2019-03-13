from textblob import TextBlob
from bs4 import BeautifulSoup
import requests

def headlines_timesnow(keyword):
	text_file = open("Output_TimesNow.txt", "w")
	for i in range(0,10):
		url = 'https://www.timesnownews.com/searchresults/0/'+ str(i) +'?searchterm={0}'.format(keyword)
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		headline_results = soup.find_all('a', class_='component_2')

		for txt in headline_results:
			headline = txt.find('div',class_="text")
			date  = txt.find('div',class_ = "datetimes")
			text_file.write("HEADLINE: "+ headline.text+"\nDATE:"+ date.text+"\n\n")
	text_file.close()

def headlines_thebetter_india(keyword):
	text_file = open("Output_TheBetterIndia.txt", "w")
	for i in range(1,2):
		url = 'https://www.thebetterindia.com/page/'+str(i)+'/?s={0}'.format(keyword)
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		headline_results = soup.find_all('li', class_="g1-collection-item")
		for txt in headline_results:
			headline = txt.find('h3')
			text_file.write("HEADLINE: "+ headline.find('a').text+"\nDATE:"+ str(txt.find('time')['datetime'])+"\nURL:"+str(headline.find('a')['href'])+"\n\n")
	text_file.close()




headlines_thebetter_india('haryana')

