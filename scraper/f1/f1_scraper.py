from scraper.helpers import Topics
from scraper.scraper_common import marca_scraper, as_scraper, mundo_deportivo_scraper, sport_scraper


def marca():
    url = "https://www.marca.com/motor/formula1.html"
    marca_scraper(Topics.F1, url)


def as_news():
    url = "https://as.com/motor/formula_1"
    as_scraper(Topics.F1, url)


def mundo_deportivo():
    url = "https://www.mundodeportivo.com/motor/f1"
    mundo_deportivo_scraper(Topics.F1, url)


def sport():
    url = "https://www.sport.es/es/motor/formula1/"
    sport_scraper(Topics.F1, url)


if __name__ == "__main__":
    marca()
    as_news()
    mundo_deportivo()
    sport()
