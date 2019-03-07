from bs4 import BeautifulSoup
import time
import glob
import requests
import os

def get_article_urls():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	
	url = 'http://www.leica.org.cn/page/1/'
	out_file = open("./out/articles.txt","w",1)	

	for i in range(1,117):
		print(i)
		link = url+str(i)
		re = requests.get(link, headers=headers)
		soup = BeautifulSoup(re.text, 'html.parser')
		for title in soup.findAll("div",{"class":"textbox-title"}):
			out_file.write(title.find("a",href=True)['href'] + '\n')
		
		



def main():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	for file_name in glob.glob("./out/*.txt"):
		article_file = open(file_name,'r')
		print(file_name)
		count = 0
		for line in article_file:
			print(count)
			count += 1
			if line[0] != 'h':
				continue
			
			
			url = line[:-1]
			name = "./out/articles/" + str(count) + '.txt'
			
			
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
			
			article = article_soup.find("div",{"class":"textbox-content article-inner-content"})	
			if article == None:
				print(url)
				continue		
			
			out_file.write(article.get_text())				
			out_file.flush()
		print(file_name + " done!")
			
	
if __name__ == '__main__':
	main()