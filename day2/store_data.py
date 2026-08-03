import pandas as pd
import numpy as np
from db import get_session
from models import Destination

df = pd.read_pickle("../day1/destinations_with_embeddings.pkl")

session = get_session()
session.query(Destination).delete()

for _, row in df.iterrows():
    embedding_array = np.array(row["embedding"], dtype=np.float32)
    dest = Destination(
        name=row["name"],
        country=row["country"],
        description=row["description"],
        category=row["category"],
        embedding=embedding_array.tobytes(),
    )
    session.add(dest)

session.commit()

count = session.query(Destination).count()
print(f"Stored {count} destinations in the database.")

session.close()