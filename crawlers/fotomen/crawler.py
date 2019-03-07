from bs4 import BeautifulSoup
import time
import glob
import requests
import os

def get_article_urls():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

	years = range(2005,2018)
	months = range(1,13)

	url = 'http://fotomen.cn'
	out_file = open("./out/articles.txt","w",1)	
	for year in years:
		for month in months:			
			print(year,month)
			
			re = requests.get(url + '/' + str(year) + '/' + str(month), headers=headers)
			soup = BeautifulSoup(re.text, 'html.parser')	
			for dl in soup.find("div",{"id":"main"}).findAll("h2",{"class":"h4"}):
				a_link = dl.find("a",href=True)['href']
				out_file.write(a_link + '\n')	
			
			next = soup.find("li",{"class":"cb-next-link"})
			while next:
				re = requests.get(next.find("a",href=True)['href'], headers=headers)
				soup = BeautifulSoup(re.text, 'html.parser')
				for dl in soup.find("div",{"id":"main"}).findAll("h2",{"class":"h4"}):
					a_link = dl.find("a",href=True)['href']
					out_file.write(a_link + '\n')
				
				next = soup.find("li",{"class":"cb-next-link"})



def main():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	for file_name in glob.glob("./out/*.txt"):
		article_file = open(file_name,'r')
		print(file_name)
		count = 0
		for line in article_file:
			print(count)
			count += 1
			if count < 240:
				continue
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
			
			article = article_soup.find("section",{"itemprop":"articleBody"})	
			if article == None:
				print(url)
				continue		
			
			out_file.write(article.get_text())
			
			for next_page in article_soup.findAll("span",{"class":"wp-link-pages-number"})[1:]:
				re = requests.get(url + next_page.get_text(), headers=headers)
				re.encoding = 'utf-8'
				article_soup = BeautifulSoup(re.text, 'html.parser')
				article = article_soup.find("section",{"itemprop":"articleBody"})
				out_file.write(article.get_text())
				
			out_file.flush()
		print(file_name + " done!")
			
	
if __name__ == '__main__':
	main()