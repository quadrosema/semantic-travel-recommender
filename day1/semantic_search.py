import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from embeddings import get_embedding


def find_similar(user_input: str, df: pd.DataFrame, top_k: int = 3):
    input_embedding = get_embedding(user_input, is_query=True).reshape(1, -1)
    stored_embeddings = list(df["embedding"])
    scores = cosine_similarity(input_embedding, stored_embeddings)[0]

    df = df.copy()
    df["score"] = scores
    return df.sort_values("score", ascending=False).head(top_k)


if __name__ == "__main__":
    df = pd.read_pickle("destinations_with_embeddings.pkl")

    queries = [
        "romantic city with art",
        "beach paradise",
        "mountain hiking",
        "modern city nightlife",
    ]

    for q in queries:
        print(f"\nQuery: '{q}'")
        results = find_similar(q, df)
        for _, row in results.iterrows():
            print(f"  {row['name']} ({row['country']}) - score: {row['score']:.3f}")