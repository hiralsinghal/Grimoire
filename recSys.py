import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

books = pd.read_csv("books.csv")
books.fillna("", inplace=True)

books['content'] = (books['title'] + " " + books['author'] + " " + books['genre'] + " " + books['description'])

vectorizer = TfidfVectorizer(stop_words='english')
bookVectors = vectorizer.fit_transform(books['content'])

similarity_matrix = cosine_similarity(bookVectors)

model = NearestNeighbors(metric='cosine')
model.fit(bookVectors)

distances, indices = model.kneighbors(bookVectors[0], n_neighbors=6)

def recSys(book_title, top_n=5):
    smallBookTitle = book_title.lower()
    bookMatches = books[books['title'].str.lower() == smallBookTitle]

    if len(bookMatches) == 0:
        print(f"Book '{book_title}' not found.")
        return None

    index = bookMatches.index[0]
    
    dist, ind = model.kneighbors(bookVectors[index], n_neighbors=top_n + 1)
    
    recIndices = ind.flatten()[1:]
    
    return books.iloc[recIndices][['title', 'author', 'genre']]

bookName = input("Enter book title: ")
recommendations = recSys(bookName)

print(recommendations)