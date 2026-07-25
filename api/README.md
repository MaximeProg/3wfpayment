# Payment Platform — API

Backend FastAPI de la Payment Platform interne (passerelle unique vers Yellow Card).
Voir [docs/cahier-des-charges.md](../docs/cahier-des-charges.md) et [docs/plan-technique.md](../docs/plan-technique.md).

## Démarrage local

```bash
cd api
python -m venv .venv
.venv/Scripts/activate       # Windows
pip install -r requirements.txt

cp .env.example .env         # puis renseigner DATABASE_URL (Neon), RESEND_API_KEY, etc.

# Redis local (pour le cache et les workers Arq)
docker compose -f ../infra/docker-compose.dev.yml up -d

# Migrations
alembic upgrade head

# Lancer l'API
uvicorn app.main:app --reload
```

- Documentation interactive : http://localhost:8000/docs
- Health check : http://localhost:8000/health
- Health check (avec vérification DB) : http://localhost:8000/health/ready

## Base de données

La base est hébergée sur **Neon** (PostgreSQL serverless) :

- `DATABASE_URL` : endpoint **pooled** (PgBouncer, mode transaction) — utilisé par l'application au runtime.
- `DATABASE_URL_DIRECT` : endpoint **direct** (non poolé) — utilisé uniquement par Alembic pour les migrations (DDL).

## Migrations

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```



