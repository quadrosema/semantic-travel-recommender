import pandas as pd
import numpy as np
from db import engine
from models import destinations

df = pd.read_pickle("../day1/destinations_with_embeddings.pkl")

with engine.begin() as conn:
    conn.execute(destinations.delete())

    rows = []
    for _, row in df.iterrows():
        embedding_array = np.array(row["embedding"], dtype=np.float32)
        rows.append({
            "name": row["name"],
            "country": row["country"],
            "description": row["description"],
            "category": row["category"],
            "embedding": embedding_array.tobytes(),
        })

    conn.execute(destinations.insert(), rows)

    stored_count = len(conn.execute(destinations.select()).fetchall())

print(f"Stored {stored_count} destinations in the database.")