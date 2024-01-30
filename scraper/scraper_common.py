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
            if body:
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

            if soup.find('div', attrs={'class': 'futbolisimos'}):
                continue

            body = soup.find('div', attrs={'class': 'art__m-cnt'})
            if body:
                create_document(topic, title, body.get_text())


def mundo_deportivo_scraper(topic: Topics, url: str):
    split_url = url.split('/')
    domain = '/'.join(split_url[:-1])
    documents = get_all_documents(topic)

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('div', attrs={'class': 'article-details'})
    for article in articles:
        link = article.find('a')
        if link:
            raw_title = link.text
            title = clean_title(raw_title)
            url_article = link.get('href')
            if title not in documents:
                response = requests.get(domain + url_article)
                soup = bs4.BeautifulSoup(response.content, 'html.parser')

                paragraphs = soup.find_all('p', attrs={'class': 'paragraph'})
                text = ' '.join([p.get_text() for p in paragraphs])
                create_document(topic, title, text)


def sport_scraper(topic: Topics, url: str):
    documents = get_all_documents(topic)

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article', attrs={'class': 'sp-noticia'})
    for article in articles:
        block = article.find('div', attrs={'class': 'txt'})
        if block:
            link = block.find('a')
            if link:
                raw_title = link.text
                title = clean_title(raw_title)
                url_article = block.find('a').get('href')
                if title not in documents:
                    response = requests.get(url_article)
                    soup = bs4.BeautifulSoup(response.content, 'html.parser')

                    paragraphs = soup.find_all('p', attrs={'class': 'ft-text'})
                    text = ' '.join([p.get_text() for p in paragraphs])
                    create_document(topic, title, text)
