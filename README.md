# ShortLink API

A backend URL shortener built with FastAPI, PostgreSQL and SQLAlchemy.

ShortLink API allows users to create shortened URLs and redirect them to their original destination while storing links persistently in PostgreSQL.

The project includes database migrations with Alembic and an automated test suite with pytest.

## Features

- Create shortened URLs
- Redirect short codes to original URLs
- PostgreSQL persistence
- Unique short-code validation
- Secure short-code generation with Python `secrets`
- Environment-based configuration
- Database migrations with Alembic
- Automated API tests with pytest
- Isolated test database
- UTC-aware timestamps
- Automatic API documentation with Swagger UI
- SQLAlchemy ORM integration

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Psycopg
- Pydantic
- Pydantic Settings
- Alembic
- pytest
- Uvicorn

## Project Structure

```text
shortlink-api/
├── alembic/
│   ├── versions/
│   │   ├── 7df68c8ed018_create_links_table.py
│   │   └── e6fc476ddda5_use_timezone_aware_timestamps.py
│   └── env.py
├── app/
│   ├── models/
│   │   └── link.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   └── test_main.py
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/silvvrodriguez/shortlink-api.git
cd shortlink-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password_here
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=shortlink
```

The `.env` file contains local configuration and must not be committed to Git.

## Database Setup

Create a PostgreSQL database named `shortlink`:

```sql
CREATE DATABASE shortlink;
```

Apply the database migrations:

```bash
alembic upgrade head
```

Alembic manages the database schema and keeps it synchronized with the application models.

To check the current migration:

```bash
alembic current
```

## Running the API

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Create a short link

```http
POST /links
```

Request body:

```json
{
  "url": "https://www.example.com"
}
```

Example response:

```json
{
  "id": 1,
  "original_url": "https://www.example.com/",
  "short_code": "Ab3Xy9",
  "short_url": "http://127.0.0.1:8000/Ab3Xy9",
  "created_at": "2026-09-14T12:00:00+00:00"
}
```

### Redirect to the original URL

```http
GET /{short_code}
```

Example:

```text
GET /Ab3Xy9
```

The API retrieves the corresponding link from PostgreSQL and redirects the client to the original URL.

If the short code does not exist, the API returns a `404 Not Found` response.

## Short Code Generation

Short codes are generated using Python's `secrets` module.

Before storing a new link, the API checks whether the generated short code already exists. If a collision is detected, another code is generated, with a limited number of attempts.

The PostgreSQL database also enforces a unique constraint on short codes.

## Database Migrations

Database schema changes are managed with Alembic.

The migration history currently includes:

- Initial `links` table creation
- Migration to timezone-aware timestamps

New migrations can be generated with:

```bash
alembic revision --autogenerate -m "migration description"
```

Then applied with:

```bash
alembic upgrade head
```

## Tests

The project includes automated tests for the main API behavior.

The test suite currently verifies:

- API health endpoint
- Short-link creation
- Redirect behavior
- `404` response for nonexistent short codes

Tests use an isolated SQLite database so they do not modify the development PostgreSQL database.

Run the test suite with:

```bash
python -m pytest
```

Current test suite:

```text
4 passed
```

## Roadmap

The current version implements the core URL-shortening functionality, database migrations and automated testing.

Possible future improvements:

- Custom aliases
- Link expiration
- Click analytics
- User authentication
- Rate limiting
- Redis caching
- Docker support
- GitHub Actions CI
- Deployment

## Author

Silvana Rodríguez

GitHub: [@silvvrodriguez](https://github.com/silvvrodriguez)