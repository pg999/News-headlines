from textblob import TextBlob
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import requests

def headlines_timesnow(keyword,no_of_pages):
	dataframe_obj = 0
	data = {'News Portal':[],'Keyword':[], 'Headlines': [],'URL':[],'Date':[]}

	for i in range(0,no_of_pages):

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
			data['Date'].append(datetime.strptime(date.text,'%b %d, %Y | %H:%M %Z').date())
			data['Keyword'].append(keyword)

		dataframe_obj = pd.DataFrame(data,columns=('News Portal','Keyword','Headlines','URL','Date'))
	return dataframe_obj

def headlines_thebetter_india(keyword,no_of_pages):
	dataframe_obj=0
	data = {'News Portal':[], 'Keyword':[],'Headlines': [],'URL':[],'Date':[]}

	for i in range(1,no_of_pages):

		url = 'https://www.thebetterindia.com/page/'+str(i)+'/?s={0}'.format(keyword)
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		headline_results = soup.find_all('li', class_="g1-collection-item")

		for item in headline_results:

			headline = item.find('h3')
			data['News Portal'].append("The Better India")
			data['Headlines'].append(headline.find('a').text)
			data['URL'].append(str(headline.find('a')['href']))
			data['Date'].append(datetime.strptime(str(item.find('time').text),'%B %d, %Y, %I:%M %p').date())
			data['Keyword'].append(keyword)

		dataframe_obj = pd.DataFrame(data,columns=('News Portal','Keyword','Headlines','URL','Date'))
	return dataframe_obj

def headlines_indiatoday(keyword,no_of_pages):
	dataframe_obj = 0
	data = {'News Portal':[], 'Keyword':[],'Headlines': [],'URL':[],'Date':[]}

	for i in range(0,no_of_pages):

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
			data['Date'].append(datetime.strptime(date.text,'Updated : %B %d, %Y, %I:%M %p').date())
			data['Keyword'].append(keyword)

			dataframe_obj = pd.DataFrame(data,columns=('News Portal','Keyword','Headlines','URL','Date'))
	return dataframe_obj

writer = pd.ExcelWriter('test.xlsx',engine='xlsxwriter')
keywords = input("Enter Keyword(Press Enter for Default):- ")

if not keywords:
	print("Default:- Haryana Cabinet Approves Delhi-Gurugram-SNB RRTS Corridor")
	keywords="Haryana Cabinet Approves Delhi-Gurugram-SNB RRTS Corridor"

no_of_pages = input("Enter No. Of Pages per news portal (Press Enter for default (2 pages) ):- ")

if not bool(no_of_pages):
	no_of_pages = 2

keywordlist = keywords.replace(',','').replace('-', ' ').split(' ')
df = pd.DataFrame()

for items in keywordlist:

	df1 = headlines_timesnow(items,no_of_pages)
	df2 = headlines_thebetter_india(items,no_of_pages)
	df3 = headlines_indiatoday(items,no_of_pages)
	df = pd.concat([df, df1, df2, df3],ignore_index=True)

df.to_excel(writer)
writer.save()
