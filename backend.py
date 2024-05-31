from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import psycopg2
from flask_cors import CORS

def get_db_connection():
    conn = psycopg2.connect(
        dbname='movie_watchlist',
        user='postgres',
        password='root',
        host='localhost',
        port='5432',
    )
    return conn

app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

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
            conn = get_db_connection()
            cur = conn.cursor()
            args = parser.parse_args()
            cur.execute(
                'INSERT INTO v1.movies (name, year, genre, director) VALUES (%s, %s, %s, %s) RETURNING id;',
                (args['name'], args['year'], args['genre'], args['director'])
            )
            movie_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return {'id': movie_id, 'name': args['name'], 'year': args['year'], 'genre': args['genre'], 'director': args['director']}, 201
        
        except Exception as e:
            return {"error": f"Internal Server error: {e}"},500

    def get(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM v1.movies;')
            movies = cur.fetchall()
            cur.close()
            conn.close()
            return {'movies':[{'id': movie[0], 'name': movie[1], 'year': movie[2], 'genre': movie[3], 'director': movie[4]} for movie in movies]},200
        except Exception as e:
            return {"error": f"Internal Server error: {e}"},500

    def delete(self, id):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM v1.movies WHERE id = %s RETURNING id;', (id,))
            deleted_id = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            if deleted_id is None:
                return {'error': 'Movie not found'}, 404
            return {'message': 'Movie deleted'},201
        except Exception as e:
            return {"error": f"Internal Server error: {e}"},500


api.add_resource(MovieResource,'/movies','/movies/<int:id>')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)
