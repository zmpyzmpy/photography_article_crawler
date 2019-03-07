from core import *
from bs4 import BeautifulSoup
import time
import glob
import requests

def get_article_urls():
	br = start_browser()
	
	url = 'https://tuchong.com/course/'
	
	br.get(url)
	out_file = open("./out/articles.txt","w")
	SCROLL_PAUSE_TIME = 1
	count = 0
	while True:
		count += 1
		br.execute_script("window.scrollTo(0, 0);")
		br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(SCROLL_PAUSE_TIME)
		print(count)
		if count > 75:
			break
		
	soup = BeautifulSoup(br.page_source, 'html.parser')
	for dl in soup.findAll("a",{"class":"item-title"},href=True):
		link = dl['href']
		out_file.write(dl['href']+'\n')

def main():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

	for file_name in glob.glob("./out/*.txt"):
		count = 0
		article_file = open(file_name,'r')
		for line in article_file:
			count += 1
			print(count)
			if line[0] != 'h':
				continue
			
			
			url = line[:-1]
			name = "./out/articles/" + file_name.split('/')[-1][:-4] + '/' + str(count) + '.txt'
			
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
			article = article_soup.find("article",{"class":"post-content"})
				
			if article == None:
				print(url)
				continue
				
			
			out_file.write(article.get_text())
			out_file.flush()

		print(file_name + " done!")
			
	
if __name__ == '__main__':
	main()