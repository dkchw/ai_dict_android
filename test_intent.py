import urllib.request
from bs4 import BeautifulSoup
import json

def search_duckduckgo(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a', class_='result__snippet'):
            print(a.text)
    except Exception as e:
        print(e)

search_duckduckgo('moon+ reader pro custom dictionary intent android')
