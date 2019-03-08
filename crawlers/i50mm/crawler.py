from bs4 import BeautifulSoup
import time
import requests
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def crawl_one_page(url, out_file):
    try:
        re = requests.get(url, headers=headers)
    except:
        time.sleep(1)
    re.encoding = 'utf-8'
    article_soup = BeautifulSoup(re.text, 'html.parser')
    article = article_soup.find("div", {"class": "entry-content"})
    out_file.write(article.get_text())
    out_file.flush()
    next_page = article_soup.find("div", {"class", "nav-previous"}).find("a", href=True)['href']

    return next_page


def main():
    count = 1
    start_url = 'http://i50mm.com/?p=5189'
    name = "./out/articles/" + str(count) + '.txt'
    directory = os.path.dirname(name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    out_file = open(name, 'w')

    next_page = crawl_one_page(start_url, out_file)

    while next_page:
        print(count)
        count += 1
        name = "./out/articles/" + str(count) + '.txt'
        out_file = open(name, 'w')

        next_page = crawl_one_page(next_page, out_file)

    print('done!')


if __name__ == '__main__':
    main()
