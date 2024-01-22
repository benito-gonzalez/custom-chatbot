from scraper.helpers import Topics
from scraper.scraper_common import marca_scraper, as_scraper


def marca():
    url = "https://www.marca.com/futbol/primera-division.html"
    marca_scraper(Topics.FOOTBALL, url)


def as_news():
    url = "https://as.com/futbol/primera"
    as_scraper(Topics.FOOTBALL, url)


if __name__ == "__main__":
    marca()
    as_news()
