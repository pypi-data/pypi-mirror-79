import requests
from bs4 import BeautifulSoup

def call():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57'}
    url = "https://www.melon.com/chart/index.htm"
    res = requests.get(url, headers=headers).text
    soup = BeautifulSoup(res, features = "html.parser")
    spans = soup.find_all("span", {"class": "checkEllipsis"})
    artists = list(set([i.text.split('(')[0].strip(' ') for i in spans]))
    return(artists)

