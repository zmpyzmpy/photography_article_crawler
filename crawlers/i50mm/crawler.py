from bs4 import BeautifulSoup
import time
import glob
import requests
import os
def main():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


	count = 1
	
	
	start_url = 'http://i50mm.com/?p=5189'
	re = requests.get(start_url, headers=headers)
	name = "./out/articles/" + str(count) + '.txt'
	
	directory = os.path.dirname(name)
	if not os.path.exists(directory):
		os.makedirs(directory)
	out_file = open(name, 'w')
	re.encoding = 'utf-8'
	article_soup = BeautifulSoup(re.text, 'html.parser')
	article = article_soup.find("div",{"class":"entry-content"})
	out_file.write(article.get_text())				
	out_file.flush()
	
	next = article_soup.find("div",{"class","nav-previous"})
	next = next.find("a",href=True)['href']
	while next:
		print(count)
		count += 1
		
		
		url = next
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
		
		article = article_soup.find("div",{"class":"entry-content"})	
		if article == None:
			print(url)
			continue		
		
		out_file.write(article.get_text())				
		out_file.flush()
		next = article_soup.find("div",{"class","nav-previous"})
		next = next.find("a",href=True)['href']

			
	
if __name__ == '__main__':
	main()