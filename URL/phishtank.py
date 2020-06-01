import re
import urllib.request
import csv
import chardet
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import time
def get_link(page):  # 寻找链接的href
    linkData = []
    for page in page.find_all('td'):
        links = page.select("a")
        for each in links:
            # if str(each.get('href'))[:1] == '/': 过滤if代码
                data=each.get('href')
                linkData.append(data)
    return(linkData)

def caiji(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'username': 'zhancat200801@sina.com', 'password': '1234'}
    headers = {'User-Agent': user_agent}
    data = urlencode(values)
    request = urllib.request.Request(url, data.encode("utf-8"), headers)
 
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page,'html.parser') #利用BeautifulSoup取得网页代码
    links=get_link(soup)
    for childLink in links:
        if(childLink.find("phish_detail.php")>-1):
            url1=urljoin(url, childLink, True)
            user_agent1 = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
            headers1 = {'User-Agent': user_agent1}
            req = urllib.request.Request(url=url1,headers=headers1)
          
            page1 = urllib.request.urlopen(req).read().decode("utf-8")
      
            soup1 = BeautifulSoup(page1,'html.parser')
            tag=soup1.find('span', attrs={"style": "word-wrap:break-word;"})
            print(tag.find('b').getText())
            time.sleep(3)
            #page1 = urllib.request.urlopen(urljoin(url, childLink, True)).read()
            #soup1 = BeautifulSoup(page1,'html.parser')
            #print(soup1)
 
if __name__ == '__main__':
    
    url = 'https://www.phishtank.com/'  # 要采集的URL
    caiji(url) 