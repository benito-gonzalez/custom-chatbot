from scraper.helpers import Topics
from scraper.scraper_common import marca_scraper, as_scraper, mundo_deportivo_scraper, sport_scraper


def marca():
    url = "https://www.marca.com/futbol.html"
    marca_scraper(Topics.FOOTBALL, url)


def as_news():
    url = "https://as.com/futbol"
    as_scraper(Topics.FOOTBALL, url)


def mundo_deportivo():
    url = "https://www.mundodeportivo.com/futbol"
    mundo_deportivo_scraper(Topics.FOOTBALL, url)


def sport():
    url = "https://www.sport.es/es/futbol/"
    sport_scraper(Topics.FOOTBALL, url)


if __name__ == "__main__":
    marca()
    as_news()
    mundo_deportivo()
    sport()
