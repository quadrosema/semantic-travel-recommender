# Semantic Travel Recommender

A retrieval project that ranks travel destinations from natural-language preferences using **BGE embeddings and cosine similarity**, with PostgreSQL storage and a Flask interface.

**Stack:** Python · Sentence Transformers · NumPy · SQLAlchemy Core · PostgreSQL · Alembic · Flask

## How it works

1. Encode a small catalog of 15 destinations using `BAAI/bge-base-en-v1.5`.
2. Store destination metadata and serialized embeddings in PostgreSQL.
3. Encode the query with BGE's retrieval instruction prefix.
4. Compare the query vector against stored destination vectors.
5. Return three recommendations, or fallback suggestions for an empty or weakly matched request.

This is embedding-based retrieval. It does not use an LLM to generate travel advice or fetch current travel information.

## Local setup

Use Python 3.10+ and a running PostgreSQL server. From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create a local database and role through PostgreSQL's administration interface, using your own password:

```sql
CREATE USER travel_user WITH PASSWORD 'YOUR_LOCAL_PASSWORD';
CREATE DATABASE travel_rec_db OWNER travel_user;
```

Set the same connection URL in **both** `day2/db.py` and `day2/alembic.ini`. The application and migration runner read separate configurations.

### Generate catalog embeddings

```powershell
cd day1
..\.venv\Scripts\python.exe embeddings.py
```

The first run downloads the BGE checkpoint. The script generates the local embedding artifact used by the database import.

### Apply migrations and import the catalog

Continue in the same terminal:

```powershell
cd ../day2
..\.venv\Scripts\python.exe -m alembic upgrade head
..\.venv\Scripts\python.exe store_data.py
```

For a fresh database, let Alembic create the table. Running `models.py` first would create the table outside migration history.

### Run the application

```powershell
..\.venv\Scripts\python.exe app.py
```

Open `http://127.0.0.1:5000` and describe a trip. The form returns destination names, countries, categories and descriptions.

## Repository map

| Path | Responsibility |
| --- | --- |
| `day1/destinations.py` | Sample catalog |
| `day1/embeddings.py` | BGE vector generation |
| `day1/semantic_search.py` | In-memory retrieval demonstration |
| `day2/models.py` | SQLAlchemy Core destination table |
| `day2/alembic/` | Schema migrations |
| `day2/store_data.py` | PostgreSQL catalog import |
| `day2/semantic_search_db.py` | Similarity ranking over stored vectors |
| `day2/fallback.py` | Empty/weak-query handling |
| `day2/app.py` | Flask form and results |

## Scope and evaluation

The catalog is deliberately small. Similarity indicates semantic closeness rather than travel suitability or recommendation confidence. Fallback results are labeled as suggestions. A larger catalog, relevance judgments, ranking metrics and environment-based database configuration would strengthen the next iteration.

## License

[MIT](LICENSE).
