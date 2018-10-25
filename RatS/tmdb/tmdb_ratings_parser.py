import math

from RatS.base.base_ratings_parser import RatingsParser
from RatS.tmdb.tmdb_site import TMDB


class TMDBRatingsParser(RatingsParser):
    def __init__(self, args):
        super(TMDBRatingsParser, self).__init__(TMDB(args), args)

    def _get_ratings_page(self, i):
        return '{url}?page={page_number}'.format(url=self.site.MY_RATINGS_URL, page_number=i)

    @staticmethod
    def _get_movies_count(movie_ratings_page):
        return int(movie_ratings_page.find('div', class_='title_header').find('a', attrs={'data-media-type': 'movie'})
                   .find('span').get_text().replace('.', ''))

    @staticmethod
    def _get_pages_count(movie_ratings_page):
        pages_count = int(movie_ratings_page.find('div', class_='title_header')
                          .find('a', attrs={'data-media-type': 'movie'}).find('span').get_text().replace('.', ''))
        return math.ceil(pages_count / 50.0)

    @staticmethod
    def _get_movie_tiles(movie_listing_page):
        return movie_listing_page.find(class_='results_page').find_all('div', class_='card')

    @staticmethod
    def _get_movie_title(movie_tile):
        return movie_tile.find(class_='title').find('a').find('h2').get_text()

    def _parse_movie_tile(self, movie_tile):
        movie = dict()
        movie['title'] = self._get_movie_title(movie_tile)
        movie['year'] = self._get_movie_year(movie_tile)
        movie[self.site.site_name.lower()] = dict()
        movie[self.site.site_name.lower()]['id'] = self._get_movie_id(movie_tile)
        movie[self.site.site_name.lower()]['url'] = self._get_movie_url(movie_tile)
        movie[self.site.site_name.lower()]['my_rating'] = self._get_movie_my_rating(movie_tile)

        return movie

    @staticmethod
    def _get_movie_id(movie_tile):
        return movie_tile.find(class_='title').find('a')['href'].split('/')[-1]

    @staticmethod
    def _get_movie_url(movie_tile):
        return 'https://www.themoviedb.org' + movie_tile.find(class_='title').find('a')['href']

    @staticmethod
    def _get_movie_my_rating(movie_tile):
        return int(movie_tile.find(class_='account_rating').get_text())

    @staticmethod
    def _get_movie_year(movie_tile):
        release_date = movie_tile.find(class_='release_date')
        if release_date:
            return int(release_date.get_text().split(' ')[-1])
        else:
            return 0
