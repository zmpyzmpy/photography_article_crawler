from bs4 import BeautifulSoup
import time
import requests
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def get_one_page_urls(url, out_file):
    re = requests.get(url, headers=headers)
    soup = BeautifulSoup(re.text, 'html.parser')
    for dl in soup.find("main", {"id": "main"}).findAll("h2", {"class": "entry-title"}):
        a_link = dl.find("a", href=True)['href']
        out_file.write(a_link + '\n')
    next_page = soup.find("a", {"class": "next page-numbers"}, href=True)
    return next_page


def get_article_urls():
    years = range(2005, 2019)
    months = range(1, 13)

    base_url = 'http://fotomen.cn'
    out_file = open("./out/articles.txt", "w", 1)
    for year in years:
        for month in months:
            print(f'{year}, f{month}')
            url = base_url + '/' + str(year) + '/' + str(month)
            next_page = get_one_page_urls(url, out_file)

            while next_page:
                url = next_page['href']
                next_page = get_one_page_urls(url, out_file)
        out_file.flush()


def get_one_page_article(url, out_file, first_page=False):
    try:
        re = requests.get(url, headers=headers)
    except:
        time.sleep(1)
    re.encoding = 'utf-8'
    article_soup = BeautifulSoup(re.text, 'html.parser')
    article = article_soup.find("section", {"class": "content entry-content"})
    if article is None:
        print(url)
        return []
    out_file.write(article.get_text())
    if first_page:
        next_page_nums = article_soup.findAll("span", {"class": "page-number"})[1:-1]
        return next_page_nums


def crawl_articles():
    article_file = open("./out/articles.txt", 'r').readlines()
    count = 0
    for line in tqdm(article_file):
        count += 1
        # if count < 240:
            # continue
        if line[0] != 'h':
            continue

        url, file_name = line[:-1], f"./out/articles/{count}.txt"
        out_file = open(file_name, 'w')
        next_page_nums = get_one_page_article(url, out_file, first_page=True)
        for next_page in next_page_nums:
            _ = get_one_page_article(url + next_page.get_text(), out_file)
        out_file.flush()
    print("done!")


if __name__ == '__main__':
    # get_article_urls()
    crawl_articles()
