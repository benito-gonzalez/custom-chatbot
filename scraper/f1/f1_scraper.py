import os
import bs4
import httpx

URL = "https://www.marca.com/motor/formula1.html?intcmp=MENUMIGA&s_kw=noticias"

my_path = os.path.abspath(os.path.dirname(__file__))
DOCUMENTS_PATH = os.path.join(my_path, "..", "..", "scraper", "documents")
documents = []


def get_all_documents():
    return os.listdir(DOCUMENTS_PATH)


def create_document(title, content):
    path = os.path.join(DOCUMENTS_PATH, title)
    with open(path, 'w') as archivo:
        archivo.write(content)


def clean_title(title):
    cleaned_string = title.strip()
    cleaned_string = cleaned_string.replace("'", "").replace('"', '')
    return cleaned_string


def marca():
    documents = get_all_documents()

    response = httpx.get(URL)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        title = clean_title(article.find(attrs={'class': 'ue-c-cover-content__headline'}).text)
        url_article = article.find(attrs={'class': 'ue-c-cover-content__link'}).get('href')
        if title not in documents:
            response = httpx.get(url_article)
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            body = soup.find('div', attrs={'class': 'ue-c-article__body'})
            create_document(title, body.get_text())


if __name__ == "__main__":
    marca()
