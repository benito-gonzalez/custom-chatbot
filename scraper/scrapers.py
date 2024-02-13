from scraper.f1.f1_scraper import (marca as marca_f1,
                                   as_news as as_news_f1,
                                   mundo_deportivo as mundo_deportivo_f1,
                                   sport as sport_f1)
from scraper.nba.nba_scraper import (marca as marca_nba,
                                     as_news as as_news_nba,
                                     mundo_deportivo as mundo_deportivo_nba,
                                     sport as sport_nba)
from scraper.football.football_scraper import (marca as marca_football,
                                               as_news as as_news_football,
                                               mundo_deportivo as mundo_deportivo_football,
                                               sport as sport_football)
from scraper.tennis.tennis_scraper import (marca as marca_tennis,
                                           as_news as as_news_tennis,
                                           mundo_deportivo as mundo_deportivo_tennis,
                                           sport as sport_tennis)


def run_scrapers():
    marca_f1()
    as_news_f1()
    mundo_deportivo_f1()
    sport_f1()
    marca_nba()
    as_news_nba()
    mundo_deportivo_nba()
    sport_nba()
    marca_football()
    as_news_football()
    mundo_deportivo_football()
    sport_football()
    marca_tennis()
    as_news_tennis()
    mundo_deportivo_tennis()
    sport_tennis()


if __name__ == "__main__":
    run_scrapers()
