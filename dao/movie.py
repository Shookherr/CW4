from config import Config
from dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Movie).get(bid)

    def get_all(self, filters):
        page = filters.get("page")       # обработка
        status = filters.get("status")   # параметров запроса

        if status is not None:
            status = status.lower()

        if status == "new" and page is not None:
            return self.session.query(Movie).order_by(Movie.year.\
                desc()).paginate(int(page), Config.ITEMS_PER_PAGE, max_per_page=Config.MAX_PAGE).items

        elif status == "new":
            return self.session.query(Movie).order_by(Movie.year.desc()).all()

        elif page is not None:
            return self.session.query(Movie).\
                paginate(int(page), Config.ITEMS_PER_PAGE, max_per_page=Config.MAX_PAGE).items

        return self.session.query(Movie).all()

    def get_by_director_id(self, val):
        return self.session.query(Movie).filter(Movie.director_id == val).all()

    def get_by_genre_id(self, val):
        return self.session.query(Movie).filter(Movie.genre_id == val).all()

    def get_by_year(self, val):
        return self.session.query(Movie).filter(Movie.year == val).all()

    def create(self, movie_d):
        ent = Movie(**movie_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        movie = self.get_one(rid)
        self.session.delete(movie)
        self.session.commit()

    def update(self, movie_d):
        movie = self.get_one(movie_d.get("id"))
        movie.title = movie_d.get("title")
        movie.description = movie_d.get("description")
        movie.trailer = movie_d.get("trailer")
        movie.year = movie_d.get("year")
        movie.rating = movie_d.get("rating")
        movie.genre_id = movie_d.get("genre_id")
        movie.director_id = movie_d.get("director_id")

        self.session.add(movie)
        self.session.commit()
