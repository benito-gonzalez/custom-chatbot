from scraper.helpers import Topics
from scraper.scraper_common import marca_scraper, as_scraper, mundo_deportivo_scraper, sport_scraper


def marca():
    url = "https://www.marca.com/tenis.html"
    marca_scraper(Topics.TENNIS, url)


def as_news():
    url = "https://as.com/tenis"
    as_scraper(Topics.TENNIS, url)


def mundo_deportivo():
    url = "https://www.mundodeportivo.com/tenis"
    mundo_deportivo_scraper(Topics.TENNIS, url)


def sport():
    url = "https://www.sport.es/es/tenis/"
    sport_scraper(Topics.TENNIS, url)


if __name__ == "__main__":
    marca()
    as_news()
    mundo_deportivo()
    sport()
