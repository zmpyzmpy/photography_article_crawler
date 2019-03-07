from core import *
from bs4 import BeautifulSoup
import time
import glob
import requests

def get_article_urls():
	br = start_browser()
	
	url = 'https://www.skypixel.com/tips'
	
	br.get(url)
	out_file = open("./out/articles.txt","w")
	SCROLL_PAUSE_TIME = 0.6
	count = 0
	last_height = br.execute_script("return document.body.scrollHeight")
	while True:
		count += 1
		br.execute_script("window.scrollTo(0, 0);")
		br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(SCROLL_PAUSE_TIME)
		print(count)
		if count >60:
			break
		
	soup = BeautifulSoup(br.page_source, 'html.parser')
	for dl in soup.findAll("a",{"class":"image-raider"},href=True):
		link = dl['href']
		out_file.write(dl['href']+'\n')

def main():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	br = start_browser()
	for file_name in glob.glob("./out/*.txt"):
		count = 0
		article_file = open(file_name,'r')
		for line in article_file:
			count += 1
			print(count)
			if line[0] != '/':
				continue
			
			
			url = 'https://www.skypixel.com' + line[:-1]
			name = "./out/articles/" + file_name.split('/')[-1][:-4] + '/' + str(count) + '.txt'
			
			br.get(url)
			try:
				article_soup = BeautifulSoup(br.page_source, 'html.parser')
			except:
				continue
			directory = os.path.dirname(name)
			if not os.path.exists(directory):
				os.makedirs(directory)
			out_file = open(name, 'w')
			
			time.sleep(2)
			article = article_soup.find("div",{"id":"app"})
			print(len(article.findAll("div")))
			out_file.write(article.get_text())

				
			if article == None:
				print(url)
				continue
				
			
			out_file.write(article.get_text())
			out_file.flush()

		print(file_name + " done!")
			
	
if __name__ == '__main__':
	main()