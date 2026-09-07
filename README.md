# For Your Favorite Human

A small birthday website built with FastAPI, PostgreSQL, vanilla HTML/CSS/JavaScript, and Docker Compose.

## Run with Docker

```bash
docker compose up --build
```

Open http://localhost:8000.

The `db` service stores wishes in PostgreSQL. The app creates the `wishes` table on startup. Stop the stack with `docker compose down`; keep the database volume by leaving off `-v`.

## Run locally

Create a PostgreSQL database named `birthday`, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The local default connection points to `localhost`. For another database, set `DATABASE_URL` before starting the server. Docker Compose injects its own connection string for the `db` service.
