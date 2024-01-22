import bs4
import requests
from scraper.helpers import get_all_documents, clean_title, create_document, Topics


def marca_scraper(topic: Topics, url: str):
    documents = get_all_documents(topic)

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        title = clean_title(article.find(attrs={'class': 'ue-c-cover-content__headline'}).text)
        url_article = article.find(attrs={'class': 'ue-c-cover-content__link'}).get('href')
        if title not in documents:
            response = requests.get(url_article)
            soup = bs4.BeautifulSoup(response.content, 'html.parser')

            # There are articles which are only a bunch of photos, we have to skip them
            if soup.find('article', attrs={'class': 'gallery-cover-article'}):
                continue

            body = soup.find('div', attrs={'class': 'ue-c-article__body'})
            create_document(topic, title, body.get_text())


def as_scraper(topic: Topics, url: str):
    documents = get_all_documents(topic)

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article', attrs={'class': 's s--v'})
    for article in articles:
        block = article.find('h2', attrs={'class': 's__tl'})
        title = clean_title(block.text)
        url_article = block.find('a').get('href')
        if title not in documents:
            response = requests.get(url_article)
            soup = bs4.BeautifulSoup(response.content, 'html.parser')

            body = soup.find('div', attrs={'class': 'art__m-cnt'})
            print(title)
            create_document(topic, title, body.get_text())
