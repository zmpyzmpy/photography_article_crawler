from core import *
from bs4 import BeautifulSoup
import time
import glob
import requests
import random

def get_article_urls():
	br = start_browser()
	
	url = 'http://weixin.sogou.com/'
	
	keywords = ['摄影','旅行','风光','人文','相机','欧洲','亚洲','美国']
	
	out_file = open("./out/articles.txt","w",1)
	
	br.get(url)
	time.sleep(30)
	
	for keyword in keywords:

		br.get(url)
		
		elem = br.find_element_by_id("query")
		elem.send_keys(keyword)
		br.find_element_by_class_name("swz").click()
		
		next = br.find_element_by_id("sogou_next")
		
		soup = BeautifulSoup(br.page_source, 'html.parser')
		for dl in soup.findAll("div",{"class":"txt-box"}):
			link = dl.find("a",href=True)['href']
			out_file.write(link+'\n')
		
		while next:
			next.click()
			
			if 'antispider' in br.current_url:
				time.sleep(60)
			
			soup = BeautifulSoup(br.page_source, 'html.parser')
			for dl in soup.findAll("div",{"class":"txt-box"}):
				link = dl.find("a",href=True)['href']
				out_file.write(link+'\n')	
			try:		
				next = br.find_element_by_id("sogou_next")
				time.sleep(5)
			except:
				break
			
			
			
if __name__ == '__main__':
	get_article_urls()