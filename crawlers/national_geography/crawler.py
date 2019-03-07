from core import *
from bs4 import BeautifulSoup
import time
import glob
import requests

def get_article_urls():
	br = start_browser()

	urls = ['http://www.nationalgeographic.com.cn/photography/picture_story/',
			'http://www.nationalgeographic.com.cn/photography/photo_of_the_day/',
			'http://www.nationalgeographic.com.cn/photography/photo_tips/',
			'http://www.nationalgeographic.com.cn/culture_list/',
			'http://www.nationalgeographic.com.cn/archive/']
			
			
	for url in urls:
		out_file = open("./out/" + url.split("/")[-2]+".txt","w")
		br.get(url)
		while True:
			try:
				br.find_element_by_class_name("load-more").click()
			except:
				break

		soup = BeautifulSoup(br.page_source, 'html.parser')
		for dl in soup.findAll("dl",{"class":"show-list-dl aside-box"}):
			out_file.write(dl.find("a",href=True)['href']+'\n')

def main():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	for file_name in glob.glob("./out/*.txt"):
		article_file = open(file_name,'r')
		for line in article_file:
			if line[0] != '/':
				continue
			
			
			url = 'http://www.nationalgeographic.com.cn' + line[:-1]
			name = "./out/articles/" + file_name.split('/')[-1][:-4] + '/' + url.split("/")[-1][:-5] + '.txt'
			
			
			try:
				re = requests.get(url, headers=headers)
			except:
				time.sleep(1)
				continue
			directory = os.path.dirname(name)
			if not os.path.exists(directory):
				os.makedirs(directory)
			out_file = open(name, 'w')
			re.encoding = 'utf-8'
			article_soup = BeautifulSoup(re.text, 'html.parser')
			
			
			article = article_soup.find("div",{"class":"show-content"})
				
			if article == None:
				article = article_soup.find("div",{"class":"M-L-pic-And-article"})
				
			
			out_file.write(article.get_text())
			out_file.flush()
		print(file_name + " done!")
			
	
if __name__ == '__main__':
	main()