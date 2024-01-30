from scraper.helpers import Topics
from scraper.scraper_common import marca_scraper, as_scraper, mundo_deportivo_scraper, sport_scraper


def marca():
    url = "https://www.marca.com/baloncesto/nba.html"
    marca_scraper(Topics.NBA, url)


def as_news():
    url = "https://as.com/baloncesto/nba"
    as_scraper(Topics.NBA, url)


def mundo_deportivo():
    url = "https://www.mundodeportivo.com/baloncesto/nba"
    mundo_deportivo_scraper(Topics.NBA, url)


def sport():
    url = "https://www.sport.es/es/nba/"
    sport_scraper(Topics.NBA, url)


if __name__ == "__main__":
    marca()
    as_news()
    mundo_deportivo()
    sport()
