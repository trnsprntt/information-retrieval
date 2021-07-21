with open('input.txt', 'r') as fin:
        url = fin.read()

loot = 'some random text'


import requests
import pprint
import re
from bs4 import BeautifulSoup
regex = r'https?:\/\/(www\.)?[-a-zA-Zа-яА-Я0-9@:%._\+~#=]{1,256}\.[a-zA-Zа-яА-Я0-9()]{1,6}\b([-a-zA-Zа-яА-Я0-9()@:%_\+.~#?&//=]*)'
visited_urls = {"http://sprotasov.ru/files/AIR/a.html"}
def find_links(html):
    urls = []

    for link in html.find_all('a'):
        urls.append(link.get('href'))

    for link in html.find_all('iframe'):
        urls.append(link.get('src'))

    for link in html.find_all('form'):
        urls.append(link.get('action'))

    result = []
    for url in urls:
        if url != None and "yandex" not in url and "ftp" not in url:
            if re.match(regex,url) and url not in visited_urls:
                result.append(url)
            elif re.match(regex,"http://sprotasov.ru/files/AIR/"+url) and "http://sprotasov.ru/files/AIR/"+url not in visited_urls:
                result.append("http://sprotasov.ru/files/AIR/"+url)
            else:
                continue
    return result

def find_loot(html):
    return "LOOT:" in str(html)

given_url = "http://sprotasov.ru/files/AIR/a.html"

def recursive_search(given_url):
    print(given_url)
    url = given_url
    req = requests.get(url, allow_redirects=True)
    if (req.status_code==200):
        html = BeautifulSoup(req.content, 'html.parser')
        loot = find_loot(html)
    if loot:
        return html
    else:
        print('hueva')
        links = find_links(html)
        print(links)
        for link in links:
            visited_urls.add(link)
            html = recursive_search(link)
    
    return html

html = recursive_search(given_url)
loot = re.search('LOOT:(.*)\\n', str(html)).group(1).strip()

with open('output.txt', 'w') as fout:
        fout.write(loot)