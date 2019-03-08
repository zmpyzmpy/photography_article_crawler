from bs4 import BeautifulSoup
import time
import requests
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
URL = 'http://www.welens.cn/article/'


def main():
    for i in range(600):

        url = URL + str(i)
        name = "./out/articles/" + str(i) + '.txt'

        try:
            re = requests.get(url, headers=headers)
        except:
            time.sleep(1)
            continue
        if re.status_code == 500:
            continue

        directory = os.path.dirname(name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        out_file = open(name, 'w')
        re.encoding = 'utf-8'
        article_soup = BeautifulSoup(re.text, 'html.parser')

        article = article_soup.find("div", {"class": "desc rich"})
        if article is None:
            print(url)
            continue

        out_file.write(article.get_text())

        out_file.flush()
        print(i)


if __name__ == '__main__':
    main()
