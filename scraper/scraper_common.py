import bs4
import logging
import requests
from scraper.helpers import get_all_documents, clean_title, create_document, Topics

logging.basicConfig(filename='/var/log/scraper.log',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.INFO)


def get_request(url):
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Getting {url} returned {response.status_code}")
        return None
    return response


def get_articles(news_source: str, topic: Topics, soup: bs4, name: str, attrs=None):
    if attrs:
        articles = soup.find_all(name, attrs=attrs)
    else:
        articles = soup.find_all(name)

    if not articles:
        logging.warning(f"There is no any news in {news_source} about {topic.value}")

    return articles


def marca_scraper(topic: Topics, url: str):
    logging.info(f'Getting news from Marca about {topic.value}')
    documents = get_all_documents(topic)

    if response := get_request(url):
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        articles = get_articles('Marca', topic, soup, 'article')
        for article in articles:
            if not (raw_title := article.find(attrs={'class': 'ue-c-cover-content__headline'})):
                logging.error(f"News title can not be retrieved for {topic.value} in Marca")
            else:
                title = clean_title(raw_title.text)
                if not (raw_link := article.find(attrs={'class': 'ue-c-cover-content__link'})):
                    logging.error(f"News link can not be retrieved for {topic.value} in Marca")
                else:
                    url_article = raw_link.get('href')
                    if title not in documents:
                        if response := get_request(url_article):
                            soup = bs4.BeautifulSoup(response.content, 'html.parser')

                            # There are articles which are only a bunch of photos, we have to skip them
                            if soup.find('article', attrs={'class': 'gallery-cover-article'}):
                                continue

                            if not (body := soup.find('div', attrs={'class': 'ue-c-article__body'})):
                                logging.error(f"News content can not be retrieved for {topic.value} in Marca")
                            else:
                                logging.info(f'Adding document "{title}" from Marca')
                                create_document(topic, title, body.get_text())


def as_scraper(topic: Topics, url: str):
    logging.info(f'Getting news from As about {topic.value}')
    documents = get_all_documents(topic)

    if response := get_request(url):
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        articles = get_articles('As', topic, soup, 'article', {'class': 's s--v'})
        for article in articles:
            if not (raw_title := article.find('h2', attrs={'class': 's__tl'})):
                logging.error(f"News title can not be retrieved for {topic.value} in As")
            else:
                title = clean_title(raw_title.text)
                if not (raw_link := raw_title.find('a')):
                    logging.error(f"News link can not be retrieved for {topic.value} in As")
                else:
                    url_article = raw_link.get('href')
                    if title not in documents:
                        if response := get_request(url_article):
                            soup = bs4.BeautifulSoup(response.content, 'html.parser')

                            if soup.find('div', attrs={'class': 'futbolisimos'}):
                                continue

                            if not (body := soup.find('div', attrs={'class': 'art__m-cnt'})):
                                logging.error(f"News content can not be retrieved for {topic.value} in As")
                            else:
                                logging.info(f'Adding document "{title}" from As')
                                create_document(topic, title, body.get_text())


def mundo_deportivo_scraper(topic: Topics, url: str):
    logging.info(f'Getting news from Mundo Deportivo about {topic.value}')
    split_url = url.split('/')
    domain = '/'.join(split_url[:3])
    documents = get_all_documents(topic)

    if response := get_request(url):
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        articles = get_articles('Mundo Deportivo', topic, soup, 'div', {'class': 'article-details'})
        for article in articles:
            if not (raw_title := article.find('a')):
                logging.error(f"News title can not be retrieved for {topic.value} in Mundo Deportivo")
            else:
                title = clean_title(raw_title.text)
                if not (url_article := raw_title.get('href')):
                    logging.error(f"News link can not be retrieved for {topic.value} in Mundo Deportivo")
                else:
                    if title not in documents:
                        if response := get_request(domain + url_article):
                            soup = bs4.BeautifulSoup(response.content, 'html.parser')

                            if not (body := soup.find('div', attrs={'class': 'article-modules'})):
                                logging.error(f"News content can not be retrieved for {topic.value} in Mundo Deportivo")
                            else:
                                logging.info(f'Adding document "{title}" from Mundo Deportivo')
                                create_document(topic, title, body.get_text())


def sport_scraper(topic: Topics, url: str):
    logging.info(f'Getting news from Sport about {topic.value}')
    documents = get_all_documents(topic)
    if response := get_request(url):
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        articles = get_articles('Sport', topic, soup, 'article', {'class': 'sp-noticia'})

        for article in articles:
            if not (block := article.find('div', attrs={'class': 'txt'})) or not block.find('a'):
                logging.error(f"News title can not be retrieved for {topic.value} in Sport")
            else:
                link = block.find('a')
                if link:
                    raw_title = link.text
                    title = clean_title(raw_title)
                    if not (url_article := block.find('a').get('href')):
                        logging.error(f"News link can not be retrieved for {topic.value} in Sport")
                    else:
                        if title not in documents:
                            if response := get_request(url_article):
                                soup = bs4.BeautifulSoup(response.content, 'html.parser')

                                if not (paragraphs := soup.find_all('p', attrs={'class': 'ft-text'})):
                                    logging.error(f"News content can not be retrieved for {topic.value} in Sport")
                                else:
                                    text = ' '.join([p.get_text() for p in paragraphs])
                                    logging.info(f'Adding document "{title}" from Sport')
                                    create_document(topic, title, text)
