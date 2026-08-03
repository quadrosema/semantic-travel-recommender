import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "day1"))

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from db import engine
from models import destinations
from embeddings import get_embedding


def find_similar_db(user_input: str, top_k: int = 3):
    input_embedding = get_embedding(user_input, is_query=True).reshape(1, -1)

    with engine.connect() as conn:
        rows = conn.execute(destinations.select()).fetchall()

    scored = []
    for row in rows:
        stored_embedding = np.frombuffer(row.embedding, dtype=np.float32).reshape(1, -1)
        score = cosine_similarity(input_embedding, stored_embedding)[0][0]
        scored.append((row, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    queries = [
        "romantic city with art",
        "beach paradise",
        "mountain hiking",
        "modern city nightlife",
    ]

    for q in queries:
        print(f"\nQuery: '{q}'")
        results = find_similar_db(q)
        for row, score in results:
            print(f"  {row.name} ({row.country}) - score: {score:.3f}")