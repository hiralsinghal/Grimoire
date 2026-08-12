from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)

# Enable CORS so your Astro frontend (running on port 4321) can talk to Flask (port 5000)
CORS(app)

# Load dataset
DATASET_PATH = 'books.csv'

def load_data():
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH)
        # Ensure consistent column naming (lowercased stripped headers)
        df.columns = [col.strip().lower() for col in df.columns]
        return df
    else:
        # Fallback dummy dataframe if books.csv isn't found
        print(f"Warning: {DATASET_PATH} not found. Using fallback sample dataset.")
        return pd.DataFrame([
            {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy"},
            {"title": "The Fellowship of the Ring", "author": "J.R.R. Tolkien", "genre": "Fantasy"},
            {"title": "Dune", "author": "Frank Herbert", "genre": "Sci-Fi"},
            {"title": "Foundation", "author": "Isaac Asimov", "genre": "Sci-Fi"},
            {"title": "1984", "author": "George Orwell", "genre": "Dystopian"},
            {"title": "Brave New World", "author": "Aldous Huxley", "genre": "Dystopian"},
        ])

df = load_data()


@app.route('/api/search_titles', methods=['GET'])
def search_titles():
    """Returns matching titles for the search dropdown autocompletion."""
    query = request.args.get('q', '').strip().lower()

    if not query or 'title' not in df.columns:
        return jsonify([])

    # Case-insensitive search for titles containing the query string
    matches = df[df['title'].astype(str).str.lower().str.contains(query, na=False)]
    
    # Return top 10 unique titles
    suggestions = matches['title'].drop_duplicates().head(10).tolist()
    return jsonify(suggestions)


@app.route('/api/recommend', methods=['GET'])
def recommend():
    """Generates book recommendations based on an input title."""
    input_title = request.args.get('title', '').strip()

    if not input_title:
        return jsonify({"error": "Please provide a book title."}), 400

    if 'title' not in df.columns:
        return jsonify({"error": "Dataset formatting error: 'title' column missing."}), 500

    # Find the input book in the dataset (exact or partial match)
    match = df[df['title'].astype(str).str.lower() == input_title.lower()]

    if match.empty:
        # Partial match fallback
        match = df[df['title'].astype(str).str.lower().str.contains(input_title.lower(), na=False)]

    if match.empty:
        return jsonify({"error": f"Book '{input_title}' not found in database."}), 404

    target_book = match.iloc[0]

    # Recommendation Logic: Match by genre or author, excluding the input book itself
    query_conditions = (df['title'].astype(str).str.lower() != target_book['title'].lower())
    
    matches = pd.DataFrame()

    if 'genre' in df.columns and pd.notna(target_book.get('genre')):
        genre_matches = df[query_conditions & (df['genre'].astype(str).str.lower() == str(target_book['genre']).lower())]
        matches = pd.concat([matches, genre_matches])

    if 'author' in df.columns and pd.notna(target_book.get('author')):
        author_matches = df[query_conditions & (df['author'].astype(str).str.lower() == str(target_book['author']).lower())]
        matches = pd.concat([matches, author_matches])

    # If no genre/author matches, fallback to random samples from the dataset
    if matches.empty:
        matches = df[query_conditions]

    # Deduplicate and limit to 6 recommendations
    recommendations = matches.drop_duplicates(subset=['title']).head(6)

    # Convert records to dictionary format
    result_list = []
    for _, row in recommendations.iterrows():
        result_list.append({
            "title": row.get('title', 'Unknown Title'),
            "author": row.get('author', 'Unknown Author'),
            "genre": row.get('genre', 'N/A')
        })

    return jsonify({"recommendations": result_list})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)