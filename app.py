from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

books = pd.read_csv("books.csv")
books.fillna("", inplace=True)

books['content'] = (books['title'] + " " + books['author'] + " " + books['genre'] + " " + books['description'])

vectorizer = TfidfVectorizer(stop_words='english')
bookVectors = vectorizer.fit_transform(books['content'])

model = NearestNeighbors(metric='cosine')
model.fit(bookVectors)

@app.route('/api/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title', '')
    small_title = title.lower()
    matches = books[books['title'].str.lower() == small_title]

    if len(matches) == 0:
        return jsonify({'error': f"Book '{title}' not found."}), 404

    index = matches.index[0]
    dist, ind = model.kneighbors(bookVectors[index], n_neighbors=6)
    rec_indices = ind.flatten()[1:]
    
    recs = books.iloc[rec_indices][['title', 'author', 'genre']].to_dict(orient='records')
    return jsonify({'recommendations': recs})

if __name__ == '__main__':
    app.run(port=5000, debug=True)