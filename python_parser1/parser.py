import os
import json
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from config import SITE_NAME, SITE_PROTOCOL
import html_cleaner
import connector


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
    try:
        os.mkdir("/home/narek/Desktop/python_parser1/"+dir_name)
    except:
        print("folder exists")


def create_html(url, folder_name,file_name):

    with open("/home/narek/Desktop/python_parser1/"+folder_name+file_name, 'w') as file:
        file.write(str(get_content(url)))
def create_json_files(folder_name,file_name,data):
    
    with open("/home/narek/Desktop/python_parser1/"+folder_name+file_name, 'w') as file:
        json.dump(data,file)
def main():

    soup = get_content(SITE_PROTOCOL + SITE_NAME)
    links = get_page_links(soup)
    # all_links=get_all_page_links(links)
    # print(len(all_links))
    create_dir("food")
    create_dir('JSON')
    for i in range(len(links)):
        create_html(SITE_PROTOCOL+SITE_NAME+links[i]['path'],'food/', f"link{i}.html")
    for data in links:
        link_data = (links.index(data)+1,data.get('path'), data.get('domain'), data.get('protocol'))
        if  link_data not in connector.select_all_links(connector.conn):

            lastrowid = connector.create_link(connector.conn, link_data[1:])
            print(lastrowid)
    connector.select_all_links(connector.conn)
    data_list=[]
    for i in links:
        s = html_cleaner.get_html_text(SITE_PROTOCOL+SITE_NAME+i['path'])
        np = html_cleaner.remove_punct(s)
        wt = html_cleaner.remove_stop_wors(np)
        wt = html_cleaner.porter(wt)
        data_list.append(html_cleaner.count_rat(wt))
        print(len(wt))
        print(data_list)
    for data in range(len(data_list)):
        create_json_files('JSON/',f'data{data}.json',data_list[data])
if __name__ == '__main__':
    main()
