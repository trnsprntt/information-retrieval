import requests
from bs4 import BeautifulSoup
import textract
import docx2python
import speech_recognition as sr
import re

loots = []

def process_txt(url):
    req = requests.get(url)
    text = req.content.decode("utf-8") 
    return re.search('LOOT:(.*)\\n', str(text)).group(1).strip()
  
def process_jpg(url):
    req = requests.get(url)
    open('file.jpg', 'wb').write(req.content)
    text = textract.process('file.jpg').decode('utf-8')
    return re.search('LO0T:(.*)\\n', str(text)).group(1).strip()

def process_pdf(url):
    req = requests.get(url)
    open('file.pdf', 'wb').write(req.content)
    text = textract.process('file.pdf').decode("utf-8") 
    return re.search('LOOT:(.*)\\n', str(text)).group(1).strip()
  
def process_docx(url):
    req = requests.get(url)
    open('file.docx', 'wb').write(req.content)
    text = docx2python.docx2python('file.docx').text
    return re.search('LOOT:(.*)\\n', str(text)).group(1).strip()

def process_html(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    text = soup.getText()
    return re.search('LOOT:(.*)\\n', str(text)).group(1).strip()
  
def process_wav(url):
    loot = ''
    req = requests.get(url)
    open('file.wav', 'wb').write(req.content)
    r = sr.Recognizer()
    with sr.AudioFile('file.wav') as s:
        r.adjust_for_ambient_noise(s, duration=1)
        loot = r.recognize_sphinx(r.record(s))
    return loot

def parse_documents():
    with open('input.txt', 'r') as fin:
        while True: 
            # Get next line from file
            line = fin.readline()
        
            # if line is empty
            # end of file is reached
            if not line:
                break
            
            url = line.strip()
            
            if '.txt' in url:
                loots.append(process_txt(url))
            elif '.jpg' in url:
                loots.append(process_jpg(url))
            elif '.pdf' in url:
                loots.append(process_pdf(url))
            elif '.docx' in url:
                loots.append(process_docx(url))
            elif '.html' in url:
                loots.append(process_html(url))
            else:
                loots.append(process_wav(url))

parse_documents()

with open('output.txt', 'w') as fout:
    for loot in loots:
      fout.write(loot)