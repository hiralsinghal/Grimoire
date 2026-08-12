"""
Flask backend for Grimoire.

Wraps the logic from recSys.py (TF-IDF + Nearest Neighbors book recommender)
behind a small JSON API, and serves the existing static site (index.html,
about.html, profile.html, css/, assets/, js) so the whole project can run
from a single `python app.py` command.
"""

import difflib
import os

import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")

# ---------------------------------------------------------------------------
# Recommendation model (built once at startup, same approach as recSys.py)
# ---------------------------------------------------------------------------

books = pd.read_csv(os.path.join(BASE_DIR, "books.csv"))
books.fillna("", inplace=True)

books["content"] = (
    books["title"] + " " + books["author"] + " " + books["genre"] + " " + books["description"]
)

vectorizer = TfidfVectorizer(stop_words="english")
bookVectors = vectorizer.fit_transform(books["content"])

model = NearestNeighbors(metric="cosine")
model.fit(bookVectors)

# lowercase title -> row index, built once for fast lookups
_title_to_index = {title.lower(): idx for idx, title in enumerate(books["title"])}

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Grimoire Recommendation API is running!"
    })

def recommend(book_title: str, top_n: int = 5):
    """
    Same behaviour as recSys() in recSys.py, but returns plain Python data
    instead of printing, so it can be turned into JSON.
    """
    index = _title_to_index.get(book_title.strip().lower())

    if index is None:
        return None

    dist, ind = model.kneighbors(bookVectors[index], n_neighbors=top_n + 1)
    rec_indices = ind.flatten()[1:]  # drop the first result (the book itself)

    results = books.iloc[rec_indices][["title", "author", "genre"]]
    return results.to_dict(orient="records")


def closest_titles(book_title: str, limit: int = 5):
    """Suggest close matches when the exact title isn't found (typos etc.)."""
    all_titles = books["title"].tolist()
    return difflib.get_close_matches(book_title, all_titles, n=limit, cutoff=0.4)


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@app.route("/api/recommend")
def api_recommend():
    title = request.args.get("title", "").strip()

    if not title:
        return jsonify({"error": "Please provide a 'title' query parameter."}), 400

    recommendations = recommend(title)

    if recommendations is None:
        return jsonify(
            {
                "found": False,
                "query": title,
                "message": f"Book '{title}' not found.",
                "suggestions": closest_titles(title),
            }
        ), 404

    return jsonify({"found": True, "query": title, "recommendations": recommendations})


@app.route("/api/books")
def api_books():
    """All titles, used for search-box autocomplete on the frontend."""
    return jsonify(sorted(books["title"].tolist()))


# ---------------------------------------------------------------------------
# Static site routes (index.html, about.html, profile.html, assets, etc.)
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)