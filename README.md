# AI Travel Recommendation App

An AI-powered travel recommendation system that understands user preferences using
semantic meaning, stores data in PostgreSQL, and returns smart recommendations using
embeddings + similarity search.

## Structure

```
Project_3/
├── day1/                          # Data prep, embeddings, semantic search (no DB)
│   ├── destinations.py            # Dataset: 15 destinations
│   ├── embeddings.py              # BGE embedding generation
│   ├── semantic_search.py         # Cosine similarity search (in-memory)
│   └── destinations_with_embeddings.pkl
├── day2/                          # Full application with PostgreSQL
│   ├── db.py                      # SQLAlchemy engine/session setup
│   ├── models.py                  # Destination table model
│   ├── alembic/                   # DB migrations
│   ├── alembic.ini
│   ├── store_data.py              # Loads Day 1 data + embeddings into Postgres
│   ├── semantic_search_db.py      # Semantic search reading from the DB
│   ├── fallback.py                # Fallback logic for empty/unmatched queries
│   └── app.py                     # Flask web app (final application)
└── requirements.txt
```

## Notes on deviations from the project brief

- **Embedding model**: uses `BAAI/bge-base-en-v1.5` (768-dim) instead of the suggested
  `all-MiniLM-L6-v2` (384-dim), for stronger retrieval quality. BGE queries are prefixed
  with `"Represent this sentence for searching relevant passages: "`; stored descriptions
  are not prefixed. This is BGE's expected usage pattern.
- **Web UI**: built with Flask instead of Streamlit (Day 2 Step 9 originally specified
  Streamlit).

## Setup

1. Clone and enter the repo:
   ```bash
   git clone https://github.com/quadrosema/Project_3.git
   cd Project_3
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:
   ```bash
   sudo -u postgres psql
   ```
   ```sql
   CREATE DATABASE travel_rec_db;
   CREATE USER travel_user WITH PASSWORD 'yourpassword';
   GRANT ALL PRIVILEGES ON DATABASE travel_rec_db TO travel_user;
   \c travel_rec_db
   GRANT ALL ON SCHEMA public TO travel_user;
   \q
   ```
   Update the connection string in `day2/db.py` and `day2/alembic.ini` if your
   credentials differ from `travel_user` / `123456` / `travel_rec_db`.

## Running it

1. Generate embeddings (Day 1) — first run downloads the BGE model (~440MB):
   ```bash
   cd day1
   python3 embeddings.py
   python3 semantic_search.py   # optional: sanity check in-memory search
   ```

2. Set up the database schema (Day 2):
   ```bash
   cd ../day2
   python3 models.py            # create the table
   alembic upgrade head         # apply migrations (if not already applied)
   ```

3. Load the data into Postgres:
   ```bash
   python3 store_data.py
   ```

4. Run the app:
   ```bash
   python3 app.py
   ```
   Open `http://127.0.0.1:5000` in a browser.

## Features

- Semantic search: understands meaning, not just keywords (e.g. "romantic city with
  art" correctly surfaces Venice even though "romantic" never appears in its description)
- Fallback logic: empty or unmatched queries return random suggestions instead of
  crashing or returning a misleading best-guess match
- Full pipeline: query → embedding → PostgreSQL similarity search → top 3 results,
  served through a Flask UI