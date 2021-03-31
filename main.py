"""
This section is to import necessary tools for the code to run well and perform necessary functions

The function of the 2 tools that are imported below are to send HTTP requests to get the HTML files of the website that we want to scrape
"""

from os import name
from numpy.core.numeric import moveaxis
import requests
from requests import get

from bs4 import BeautifulSoup as bs #BeautifulSoup is used to parse HTML files
import pandas as pd # pandas is used to assemble the data into a DataFrame to clean and analyze it 
import numpy as np # numpy is used to provide suuport for maths functions and tools for working with arrays


"""
This part of the code is to ensure we only get English language titles from the data that is scraped
More information @ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language
"""
headers = {"Accept-Language" : "en-US, en;q=0.5"}

"""
This section gets the contents of the page by requesting the URL
"""
url = "https://www.imdb.com/search/title/?groups=top_1000" # URL of the website we want to scrape
results = requests.get(url,headers=headers) # Method used to get contents of the URL

soup = bs(results.text, "html.parser")

#Initializing empty lists to stored scraped data
titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_div = soup.find_all('div', class_='lister-item mode-advanced')
for container in movie_div:
    titles.append(container.h3.a.text)
    years.append(container.h3.find('span', class_ = 'lister-item-year').text)
    time.append(container.find('span',class_='runtime').text if container.p.find('span', class_='runtime') else "-")
    imdb_ratings.append(float(container.strong.text))
    metascores.append(container.find('span', class_='metascore').text if container.find('span', class_='metascore') else "-")
    nv = container.find_all('span', attrs={'name': 'nv'})
    votes.append(nv[0].text)
    us_gross.append(nv[1].text if len(nv)>1 else "-")

movies = pd.DataFrame({
    'Movie' :titles,
    'Year': years,
    'timeMin': time,
    'IMDB': imdb_ratings,
    'Metascore': metascores,
    'Votes':votes,
    'US_GrossMillions': us_gross,
})

movies['Year'] = movies['Year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['Metascore'] = movies['Metascore'].astype(int)
movies['Votes'] = movies['Votes'].str.replace(',' , '').astype(int)
movies['US_GrossMillions'] = movies['US_GrossMillions'].map(lambda x:x.lstrip('$').rstrip('M'))
movies['US_GrossMillions'] = pd.to_numeric(movies['US_GrossMillions'], errors='coerce')

movies.to_csv() # to be updated