from scraper.helpers import Topics
from scraper.scraper_common import marca_scraper, as_scraper


def marca():
    url = "https://www.marca.com/baloncesto/nba.html"
    marca_scraper(Topics.NBA, url)


def as_news():
    url = "https://as.com/baloncesto/nba"
    as_scraper(Topics.NBA, url)


if __name__ == "__main__":
    marca()
    as_news()
