from bs4 import BeautifulSoup
import time
import glob
import requests
import os

def get_article_urls():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

	urls = ['https://www.photoworld.com.cn/category/news',
			'https://www.photoworld.com.cn/category/images',
			'https://www.photoworld.com.cn/category/gears',
			'https://www.photoworld.com.cn/category/tutorials']
			
			
	for url in urls:
		print(url)
		out_file = open("./out/" + url.split("/")[-1]+".txt","w")
		re = requests.get(url, headers=headers)
		soup = BeautifulSoup(re.text, 'html.parser')
		
		
		a = soup.findAll("a",{"class":"page-numbers"})[-2].get_text()		
		
		for i in range(1, int(a) + 1):
			print("page: " + str(i))
			try:
				r = requests.get(url + '/page/' + str(i), headers=headers)
				soup = BeautifulSoup(r.text, 'html.parser')
				for dl in soup.findAll("div",{"class":"table g3"}):
					a_link = dl.find("a",href=True)['href']
					out_file.write(a_link + '\n')
				
			except:
				break



def main():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	for file_name in glob.glob("./out/*.txt"):
		article_file = open(file_name,'r')
		print(file_name)
		count = 1
		for line in article_file:
			print(count)
			count += 1
			if line[0] != 'h':
				continue
			
			
			url = line[:-1]
			name = "./out/articles/" + file_name.split('/')[-1][:-4] + '/' + url.split("/")[-1] + '.txt'
			
			
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
			
			
			article = article_soup.find("div",{"class":"single-content"})
				
			if article == None:
				print(url)
				continue
				
			
			out_file.write(article.get_text())
			out_file.flush()
		print(file_name + " done!")
			
	
if __name__ == '__main__':
	main()