import requests
import json
import urllib
from bs4 import BeautifulSoup as bs
import csv
from datetime import date

class weatherGetter:
	def __init__(self,locations):
		self.writeDir = '.'
		self.locations = locations
		self.baseUrl = 'https://www.bbc.co.uk/weather/'
	def completeURLfromAPI(self):
		urls= []
		for loc in self.locations:
			resp = requests.get('https://locator-service.api.bbci.co.uk/locations?api_key=AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv&stack=aws&locale=en&filter=international&place-types=settlement%2Cairport%2Cdistrict&order=importance&s='+loc+'&format=json')
			if resp.ok==True:
				json_data=resp.json()['response']
				if json_data['totalResults'] ==0:
					print('Error: No location of that name: ',loc)
			
				try:
					locInfo = json_data['locations'][0]
				except:
					print('error ln24')
				
				if locInfo['container']=='Postcode District':
					urls.append(self.baseUrl+loc)
				else:
					
					
					urls.append(self.baseUrl+str(locInfo['id']))
			else:
				print('Error contacting the server')
		return urls
	def getCurrentWeather(self,urls):
		weathers = []
		for url in urls:
			
			resp=urllib.request.urlopen(url)
			html = resp.read()
			soup=bs(html)
			f=soup.findAll('div',{'class':'wr-weather-type__icon'})
			try:
				weathers.append(f[0]['title'])
			except:
				print('error with the website')
		
		zipres = dict(zip(self.locations, weathers))
		return zipres
	def writeToCSV(self,zipres):
		try:
			res = []
			with open(self.writeDir+'/res.csv','r') as f:
				reader = csv.reader(f)
				for row in reader:
					res.append(row)
			with open(self.writeDir+'/res.csv','w') as f:
				writer = csv.writer(f)
				for k in zipres.keys():
					writer.writerow([k,date.today().strftime("%d/%m/%Y"),zipres[k]])
			print('sucessfully saved')
		except:
			with open(self.writeDir+'/res.csv','w') as f:
				pass
			res = []
			with open(self.writeDir+'/res.csv','r') as f:
				reader = csv.reader(f)
				for row in reader:
					res.append(row)
			with open('res.csv','w') as f:
				writer = csv.writer(f)
				for k in zipres.keys():
					writer.writerow([k,date.today().strftime("%d/%m/%Y"),zipres[k]])
			print('sucessfully saved')

			
#This is a cool use case		
'''					
if __name__=='__main__':
	
	html = urllib.request.urlopen('https://geographyfieldwork.com/WorldCapitalCities.htm').read()
	soup = bs(html)
	f=soup.findAll('td')
	cities = []
	i = 1
	for c in f:
		if i %2 ==0:
			cities.append(c.text)
		i+=1
	print(cities)

	g= weatherGetter(cities)
	urls = g.completeURLfromAPI()
	r = g.getCurrentWeather(urls)
	g.writeToCSV(r)
	
	print('done')
	'''