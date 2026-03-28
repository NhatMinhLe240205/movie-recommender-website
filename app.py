from flask import Flask, jsonify, request
from flask_cors import CORS
from data_loader import MovieDatabase
from recommender import ContentBaseRecommender, CollaborativeRecommender
import os

app = Flask(__name__)
CORS(app)

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data')

db = MovieDatabase(DATA_PATH)
db.load_database()

content_rec = ContentBaseRecommender(db)
collab_rec  = CollaborativeRecommender(db)

print("✅ Ready!")

@app.route('/api/search')
def search():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    results = db.search_movies(q, limit=8)
    return jsonify(results)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data     = request.get_json(force=True)
    movie_id = data.get('movieId')
    method   = data.get('method', 'content')
    year     = data.get('year')

    if movie_id is None:
        return jsonify({'error': 'movieId is required'}), 400

    movie_df = db.get_movie_by_id(int(movie_id))
    if movie_df.empty:
        return jsonify({'error': 'Movie not found'}), 404

    if method == 'collaborative':
        results = collab_rec.recommend(movie_df)
    else:
        if year is None:
            return jsonify({'error': 'year is required'}), 400
        results = content_rec.recommend(movie_df, int(year))

    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)