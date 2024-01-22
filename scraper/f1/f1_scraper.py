from scraper.helpers import Topics
from scraper.scraper_common import marca_scraper, as_scraper


def marca():
    url = "https://www.marca.com/motor/formula1.html"
    marca_scraper(Topics.F1, url)


def as_news():
    url = "https://as.com/motor/formula_1"
    as_scraper(Topics.F1, url)


if __name__ == "__main__":
    marca()
    as_news()
