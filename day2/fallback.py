import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "day1"))

from db import engine
from models import destinations
from semantic_search_db import find_similar_db

SIMILARITY_THRESHOLD = 0.35


def get_fallback_recommendations(category: str = None, top_k: int = 3):
    """Fallback: return random destinations, optionally filtered by category."""
    query = destinations.select()
    if category:
        query = query.where(destinations.c.category.ilike(category))

    with engine.connect() as conn:
        all_matches = conn.execute(query).fetchall()

    if not all_matches:
        return []

    return random.sample(all_matches, min(top_k, len(all_matches)))


def recommend(user_input: str, top_k: int = 3):
    """
    Main entry point with fallback handling.
    Returns (results, used_fallback: bool, message: str)
    """
    if not user_input or not user_input.strip():
        fallback = get_fallback_recommendations(top_k=top_k)
        return fallback, True, "No input given — here are some popular picks instead:"

    results = find_similar_db(user_input, top_k=top_k)

    if not results or results[0][1] < SIMILARITY_THRESHOLD:
        fallback = get_fallback_recommendations(top_k=top_k)
        return fallback, True, f"No strong match found for '{user_input}' — here are some suggestions instead:"

    return [r[0] for r in results], False, None


if __name__ == "__main__":
    test_inputs = ["", "Haya", "asdkjaskjd", "romantic city with art"]

    for inp in test_inputs:
        print(f"\nInput: '{inp}'")
        results, used_fallback, message = recommend(inp)
        if message:
            print(f"  {message}")
        for row in results:
            print(f"  - {row.name} ({row.country})")