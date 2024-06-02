from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Mock database - in-memory array to store movie records
movies = []

# Request parser setup
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help="Title cannot be blank!")
parser.add_argument('year', type=int, required=True, help="Year cannot be blank!")
parser.add_argument('genre', type=str)
parser.add_argument('director', type=str)

# MovieResource for handling /movies/<id> endpoint
class MovieResource(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            movie = {
                'id': len(movies) + 1,  # Generate unique ID
                'name': args['name'],
                'year': args['year'],
                'genre': args['genre'],
                'director': args['director']
            }
            movies.append(movie)
            return movie, 201
        except Exception as e:
            return {"error": f"Internal Server error: {e}"}, 500

    def get(self):
        try:
            return {'movies': movies}, 200
        except Exception as e:
            return {"error": f"Internal Server error: {e}"}, 500


api.add_resource(MovieResource,'/movies','/movies/<int:id>')

if __name__ == '__main__':
    app.run()
