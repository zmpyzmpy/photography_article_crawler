import requests
from bs4 import BeautifulSoup
import os
import sys
import time
from random import randint
sys.stdout = open('log.log', 'w', 1)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
def crawl_save_page(wechat_id, article_id):
	file_path = "./output/wechat/" + wechat_id + '/' + article_id.split("/")[-1] + '.txt'
	directory = os.path.dirname(file_path)
	if not os.path.exists(directory):
		os.makedirs(directory)
	out_file = open(file_path, 'w')
	while True:
		try:
			re = requests.get('http://chuansong.me' + article_id, headers=headers)
		except:
			print("failed to request page " + article_id)
			out_file.close()
			os.remove(file_path)
			return
			
		if re.status_code != 200 and re.status_code != 403 and re.status_code != 503:
			print("failed to request page " + article_id + " with code " + str(re.status_code))
			out_file.close()
			os.remove(file_path)
			return
		if re.status_code == 403 or re.status_code == 503:
			print("sleeping... subpage " + article_id)
			time.sleep(randint(5,10))
			continue
		if re.status_code == 200:
			time.sleep(0.5)
			break
		
	article_soup = BeautifulSoup(re.text, 'html.parser')
	
	for p in article_soup.findAll("p"):
		out_file.write(p.getText() + '\n')
	
	out_file.flush()
	out_file.close()
	

def crawl_wechat(wechat_id):
	page = 0
	while True:

		try:
			r  = requests.get('http://chuansong.me/account/' + wechat_id + "?start=" + str(page), headers=headers)
			if r.status_code != 200 and r.status_code != 403:
				print("failed to request wechat " + wechat_id + "with code" + str(r.status_code))
				break
			if r.status_code == 403:
				print("sleeping... wechat " + wechat_id +" " + str(r.status_code))
				time.sleep(1)
				continue
			soup = BeautifulSoup(r.text, 'html.parser')
			for a in soup.findAll("a",{"class":"question_link"},href=True):
				crawl_save_page(wechat_id, a['href'])
			
				page += 1
				
				print(wechat_id + ": " + str(page))
		except Exception as ex:
			print(ex)
			print("end crawling " + wechat_id)
			break
		



def main():
	try:
		for line in open("./wechat_list",'r'):
			wechat_id = line[:-1]
			print(wechat_id)
			crawl_wechat(wechat_id)
	except:
		print("please input a wechat_id")
	


if __name__ == '__main__':
	main()
