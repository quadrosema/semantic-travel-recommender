from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from destinations import destinations

MODEL_NAME = "BAAI/bge-base-en-v1.5"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

model = SentenceTransformer(MODEL_NAME)


def get_embedding(text: str, is_query: bool = False) -> np.ndarray:
    if is_query:
        text = QUERY_PREFIX + text
    return model.encode(text, normalize_embeddings=True)


if __name__ == "__main__":
    df = pd.DataFrame(destinations)
    df["embedding"] = df["description"].apply(lambda x: get_embedding(x, is_query=False).tolist())

    print("Embedding shape:", np.array(df["embedding"].iloc[0]).shape)
    print("First 10 values (Paris):", df["embedding"].iloc[0][:10])

    df.to_pickle("destinations_with_embeddings.pkl")
    print(f"\nSaved {len(df)} destinations with embeddings to destinations_with_embeddings.pkl")