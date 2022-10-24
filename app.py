from flask import request
from flask_restx import Api, Resource
from schemas import MovieSchema
import json

from config import app, db
from models import Movie

api = Api(app)

movie_ns = api.namespace("movies")
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")


@movie_ns.route('/')
class MoviesViews(Resource):
    def get(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        query = Movie.query
        if director_id is not None:
            query = query.filter(Movie.director_id == director_id)
        if genre_id is not None:
            query = query.filter(Movie.genre_id == genre_id)
        return MovieSchema(many=True).dump(query.all()), 200


    def post(self):
        data = request.json
        try:
            db.session.add(
            Movie(**data)
            )
            db.session.commit()
            return "Я пожилой чак-чак!", 201

        except Exception as ex:
            db.session.rollback()
            return "Неуспешно!", 500


@movie_ns.route('/<int:id>/')
class MoviesViews(Resource):
    def get(self, id):
        result = Movie.query.filter(Movie.id == id).one()
        if result:
            return MovieSchema.dump(result), 200
        else:
            return json.dumps({}), 200


    def put(self, id):
        data = request.json
        try:
            result = Movie.query.filter(Movie.id == id).one()
            print(result)
            result.title = data.get("title")
            db.session.commit()
            return "Обновилось", 200
        except Exception as ex:
            print(ex)
            db.session.rollback()
            return "Не обновилось", 200

    def delete(self, id):
        try:
            result = Movie.query.filter(Movie.id == id).one()
            db.session.delete(result)
            return "Уничтожено", 200
        except Exception as ex:
            print(ex)
            db.session.rollback()
            return "Не уничтожено", 200



if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
