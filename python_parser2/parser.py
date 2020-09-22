import os

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from config import SITE_NAME, SITE_PROTOCOL
import html_cleaner
import connector
from sql import sql_create_words_table
from config import DATABASE_WORDS
def get_content(url):
    data = requests.get(url)
    if str(data.status_code).startswith("2"):
        soup = BeautifulSoup(data.text, 'html.parser')
        return soup


def get_page_links(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        o = urlparse(href)

        if o.path:
            flag = False
            if o.netloc == SITE_NAME or not o.netloc:
                flag = True
                if len(links) > 0:
                    # այս մասում տունը մտածել այլ տարբերակ
                    for data in links:
                        if data.get('path') == o.path:
                            flag = False

            if flag:
                links.append(
                    {'protocol': o.scheme, 'domain': o.netloc, 'path': o.path})

    return links


def get_all_page_links(links_list):
    for i in links_list:
        soup = get_content(SITE_PROTOCOL+SITE_NAME+i['path'])
        page_links = get_page_links(soup)
        for j in page_links:

            if j not in links_list:
                if j['protocol'] == 'https':
                    links_list.append(j)
                    print(j['path'])
                    print(j)
                    print(len(links_list))
    return links_list


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(os.path.join("/home/narek/Desktop/python_parser1/",dir_name))
        print('folder was created')
    else:
        print('folder exists')
    


def create_html(url, folder_name,file_name):

    with open(os.path.join("/home/narek/Desktop/python_parser1/",folder_name,file_name), 'w') as file:
        file.write(str(get_content(url)))

def main():

    soup = get_content(SITE_PROTOCOL + SITE_NAME)
    links = get_page_links(soup)
    # all_links=get_all_page_links(links)
    # print(len(all_links))
    create_dir("food")
    
    for i in range(len(links)):
        create_html(SITE_PROTOCOL+SITE_NAME+links[i]['path'],'food', f"link{i}.html")
    for data in links:
        link_data = (links.index(data)+1,data.get('path'), data.get('domain'), data.get('protocol'))
        if  link_data not in connector.select_all_links(connector.conn,"links"):
            lastrowid = connector.create_link(connector.conn, link_data[1:])
            print(lastrowid)
            print(connector.select_all_links(connector.conn,"links"))
    connector.select_all_links(connector.conn,'links')
    data_list=[]
    for i in links:
        s = html_cleaner.get_html_text(SITE_PROTOCOL+SITE_NAME+i['path'])
        np = html_cleaner.remove_punct(s)
        wt = html_cleaner.remove_stop_wors(np)
        wt = html_cleaner.porter(wt)
        data_list.append(html_cleaner.count_rat(wt,SITE_PROTOCOL+SITE_NAME+i['path']))
        print(len(wt))
        print(data_list)
        conn1 = connector.create_connection(DATABASE_WORDS)
        if conn1 is not None:
            connector.create_table(conn1, sql_create_words_table)
        for i in range(len(data_list)):
            for j in data_list[i]:
                if  (j,data_list[i][j],i+1) not in connector.select_all_links(conn1,"words"):
                    print(connector.create_word(conn1,(j,data_list[i][j],i+1)))
            print(connector.select_all_links(conn1,"words"))
if __name__ == '__main__':
    main()
