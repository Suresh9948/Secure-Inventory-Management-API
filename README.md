# Secure Inventory Management API

FastAPI, SQLAlchemy 2, MySQL, Alembic, Pydantic, Argon2 password hashing, JWT access tokens, rotating/revocable refresh tokens, and Admin/Manager/Employee RBAC.

## Setup (Windows PowerShell)

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env`, set a strong JWT secret and MySQL URL, and create the database first.

Generate a secret:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## Migrations

This package includes an example migration for the authentication tables. If integrating into an existing inventory project, set its `down_revision` to your existing latest revision and review the migration. Do not edit already-applied migrations or replace your existing inventory schema. Back up data before applying schema changes.

```powershell
alembic upgrade head
```

Run:
```powershell
uvicorn app.main:app --reload
```
Docs: http://127.0.0.1:8000/docs

## Endpoints

- `POST /api/v1/auth/register` — new accounts are always Employee.
- `POST /api/v1/auth/login` — OAuth2 form fields `username` and `password`.
- `POST /api/v1/auth/refresh` — JSON `{"refresh_token":"..."}`; rotates refresh token.
- `POST /api/v1/auth/logout` — JSON `{"refresh_token":"..."}`.
- `GET /api/v1/users/me` — current profile.
- `GET /api/v1/users` — Admin only.
- `PATCH /api/v1/users/{user_id}/role` — Admin only.
- `PATCH /api/v1/users/{user_id}/status` — Admin only.
- `/api/v1/products` — all authenticated roles can read; Admin/Manager can create/update; Admin can delete.
- `/api/v1/categories` and `/api/v1/suppliers` — all authenticated roles can read; Admin can write/delete.
- `/api/v1/reports/inventory` and `/api/v1/reports/restocking` — Admin/Manager.

## First Admin

Registration intentionally cannot create Admin. Promote a verified account only via a controlled provisioning procedure. Check the actual MySQL Enum labels before running a SQL update; do not expose a public Admin-registration endpoint.

## Security notes

- Keep `.env` out of Git.
- Use HTTPS, login rate limiting, audit logging, and secret management in production.
- Refresh tokens are stored by JTI and rotated on refresh.
- Protected requests read role and active status from the database.
- This is a reference scaffold. Merge your actual existing inventory models and migrations, then add full API integration tests before production use.

## Tests

```powershell
pytest -v
```
