import sys
import nltk
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
    text_list = [text.text for text in soup.find_all(
        ['p', 'title', 'li', 'h1', 'h2', 'a'])]
    text_string = ''
    for i in text_list:
        text_string = text_string+" "+i
    return text_string


TBL = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P'))


def remove_punct(text):
    return text.translate(TBL)


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


def count_rat(text_list):
    words_dict = {}
    for elem in text_list:
        words_dict[elem] = words_dict.get(elem, 0) + 1
    return words_dict
