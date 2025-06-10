import sqlite3

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def load_grant_texts(db_path="grants.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM grants")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "text": row[1]} for row in rows]

def extract_keywords(query, top_n=5):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([query])
    scores = np.array(tfidf_matrix.sum(axis=0)).flatten()
    terms = np.array(vectorizer.get_feature_names_out())
    sorted_indices = np.argsort(scores)[::-1]
    return terms[sorted_indices][:top_n]

def enhance_query(query, keywords, weight=2):
    words = query.split()
    enhanced = []
    for word in words:
        if word.lower() in keywords:
            enhanced.extend([word] * weight)
        else:
            enhanced.append(word)
    return " ".join(enhanced)

def find_most_similar(query_vector, text_vectors, top_n=3):
    similarities = cosine_similarity(query_vector, text_vectors)[0]
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    return top_indices, similarities[top_indices]

def search_grants(query, db_path="grants.db", weight=20, top_keywords=5, top_n=10):
    database = load_grant_texts(db_path)
    if not database:
        print("Database is empty.")
        return []

    texts = [entry["text"] for entry in database]
    ids = [entry["id"] for entry in database]

    text_vectors = model.encode(texts)
    keywords = extract_keywords(query, top_keywords)
    enhanced_query = enhance_query(query, keywords, weight)
    query_vector = model.encode([enhanced_query])

    top_indices, _ = find_most_similar(query_vector, text_vectors, top_n)
    return [ids[i] for i in top_indices]
