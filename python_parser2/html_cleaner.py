import sys
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import unicodedata
import requests

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from config import SITE_NAME, SITE_PROTOCOL
from nltk.tokenize import word_tokenize


def get_html_text(link):
    data = requests.get(link)
    if str(data.status_code).startswith("2"):
        document = data.content.decode("utf-8")
        soup = BeautifulSoup(document, 'html.parser')
        text_string = str(soup.text)
        
    return text_string


def remove_punct(text):
    for i in text:
        if not i.isalpha() and i!=" ": 
            text=text.replace(i,'')
    return text


def remove_stop_wors(text):
    wt = word_tokenize(text)
    stop_words = stopwords.words('english')
    for i in wt:
        if i in stop_words:
            wt.remove(i)
    return wt


def porter(tokenized_words):
    porter = PorterStemmer()
    stem = [porter.stem(word) for word in tokenized_words]
    return stem
def tags_word(link,tag):
    
    data = requests.get(link)
    if str(data.status_code).startswith("2"):
        document = data.content.decode("utf-8")
        soup = BeautifulSoup(document, 'html.parser')
        string=''
        for text in soup.find_all(tag):
            string+=text.text
    return string
def count_rat(text_list,link):
    tags_list=['p','h6','h5','h4','h3','h2','h1','title']
    words_dict = {}
    words_list=[]
    for tag in tags_list:
        words_list.append(tags_word(link,tag))
    for elem in text_list:
        words_dict[elem] = words_dict.get(elem, 0) + 1
        for tag in words_list:
            if elem in tag:
                   words_dict[elem] = words_dict.get(elem, 0) + round((words_list.index(tag)+1)/100*tag.count(elem),3)
            
    return words_dict
