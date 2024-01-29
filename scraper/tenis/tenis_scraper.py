from scraper.helpers import Topics
from scraper.scraper_common import marca_scraper, as_scraper


def marca():
    url = "https://www.marca.com/tenis.html"
    marca_scraper(Topics.TENNIS, url)


def as_news():
    url = "https://as.com/tenis"
    as_scraper(Topics.TENNIS, url)


if __name__ == "__main__":
    marca()
    as_news()
