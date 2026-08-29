# Database setup — Prantik (DBMS Lead)

## 1. Create the project database

Open pgAdmin 4 → right-click **Databases** → **Create** → **Database**.
Name it `airfare_index_dev`.

Or from Terminal:
```
createdb airfare_index_dev
```

## 2. Set up your Python environment

From the `backend/` folder:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-db.txt
```

## 3. Configure your database connection

```
cp backend/.env.example backend/.env
```
Edit `backend/.env` and set your actual Postgres password (the one you chose
during install) in the `DATABASE_URL` line.

## 4. Run the first migration

From `database/migrations/`:
```
alembic revision --autogenerate -m "create initial schema"
alembic upgrade head
```

This creates all 7 tables (`airports`, `airlines`, `routes`, `flights`,
`price_observations`, `index_values`, `data_sources`) in Postgres, based on
the models in `backend/app/models/`.

Check it worked: open pgAdmin → `airfare_index_dev` → Schemas → public →
Tables. You should see all 7 tables listed.

## 5. Load sample data (optional, for testing)

From `backend/` (with venv activated):
```
python ../database/seed/seed_data.py
```

## Folder ownership

```
database/
├── migrations/   ← you own this (schema versioning)
└── seed/         ← you own this (test data)

backend/app/models/  ← you own this (table definitions)
```

Nobody else should edit `backend/app/models/` or `database/migrations/`
directly — per the doc's rule: **PRANTIK OWNS THE DATABASE SCHEMA.**
Anmol, Abhay, and Guntaas import these models to query the DB, but schema
changes go through you.

## Making a schema change later

1. Edit the relevant model file in `backend/app/models/`
2. From `database/migrations/`, run:
   ```
   alembic revision --autogenerate -m "describe the change"
   alembic upgrade head
   ```
3. Commit both the model change and the new migration file together.
