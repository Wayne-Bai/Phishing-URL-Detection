from selenium import webdriver
from urllib.parse import urlparse
import time
browser = webdriver.Firefox()
url="http://www.baidu.com"
my_url = urlparse(url)
domain = '{uri.netloc}'.format(uri=my_url)

browser.get(url)
path="d:\\"+domain+"_"+time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))+".png"
print(path)
browser.save_screenshot(path)
browser.close()