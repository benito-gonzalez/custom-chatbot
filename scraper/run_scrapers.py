from scraper.f1.f1_scraper import marca as marca_f1, as_news as as_news_f1
from scraper.nba.nba_scraper import marca as marca_nba, as_news as as_news_nba
from scraper.football.football_scraper import marca as marca_football, as_news as as_news_football


def run_all_scrapers():
    marca_f1()
    as_news_f1()
    marca_nba()
    as_news_nba()
    marca_football()
    as_news_football()


if __name__ == "__main__":
    run_all_scrapers()
