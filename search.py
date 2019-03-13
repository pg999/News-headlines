from textblob import TextBlob
from bs4 import BeautifulSoup
import pandas as pd
import requests
def headlines_timesnow(keyword):
	dataframe_obj = 0
	data = {'News Portal':[], 'Headlines': [],'URL':[],'Date':[]}
	for i in range(0,10):
		url = 'https://www.timesnownews.com/searchresults/0/'+ str(i) +'?searchterm={0}'.format(keyword)
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		headline_results = soup.find_all('a', class_='component_2')
		for item in headline_results:
			headline = item.find('div',class_="text")
			date  = item.find('div',class_ = "datetimes")
			data['News Portal'].append("Times Now")
			data['Headlines'].append(headline.text)
			data['URL'].append(str(item['href']))
			data['Date'].append(date.text)
		dataframe_obj = pd.DataFrame(data,columns=('News Portal','Headlines','URL','Date'))
	return dataframe_obj

def headlines_thebetter_india(keyword):
	dataframe_obj=0
	data = {'News Portal':[], 'Headlines': [],'URL':[],'Date':[]}
	for i in range(1,11):
		url = 'https://www.thebetterindia.com/page/'+str(i)+'/?s={0}'.format(keyword)
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		headline_results = soup.find_all('li', class_="g1-collection-item")
		for item in headline_results:
			headline = item.find('h3')
			data['News Portal'].append("The Better India")
			data['Headlines'].append(headline.find('a').text)
			data['URL'].append(str(headline.find('a')['href']))
			data['Date'].append(str(item.find('time').text))
		dataframe_obj = pd.DataFrame(data,columns=('News Portal','Headlines','URL','Date'))
	return dataframe_obj

def headlines_indiatoday(keyword):
	dataframe_obj = 0
	data = {'News Portal':[], 'Headlines': [],'URL':[],'Date':[]}
	for i in range(0,10):
		url = 'https://www.indiatoday.in/topic/{0}?page='.format(keyword)+str(i)
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		headline_results = soup.find_all('li', {"class":"itg-search-list"})
		for item in headline_results:
			headline = item.find('div',class_="front-label")
			link = headline.find('a')['href']
			date = item.find('div',class_="front-search-date-share")
			data['News Portal'].append("India Today")
			data['Headlines'].append(headline.text)
			data['URL'].append(str(link))
			data['Date'].append(str(date.text))
			dataframe_obj = pd.DataFrame(data,columns=('News Portal','Headlines','URL','Date'))
	return dataframe_obj

writer = pd.ExcelWriter('test.xlsx',engine='xlsxwriter')
df1 = headlines_timesnow('haryana')
df2 = headlines_thebetter_india('haryana')
df3 = headlines_indiatoday('haryana')
df = pd.concat([df1, df2, df3],ignore_index=True)
df.to_excel(writer)
writer.save()
