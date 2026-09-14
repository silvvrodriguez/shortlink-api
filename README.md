# ShortLink API

A backend URL shortener built with FastAPI, PostgreSQL and SQLAlchemy.

ShortLink API allows users to create shortened URLs and redirect them to their original destination while storing all links persistently in PostgreSQL.

## Features

- Create shortened URLs
- Redirect short codes to original URLs
- PostgreSQL persistence
- Unique short-code validation
- Secure short-code generation with Python `secrets`
- Environment-based configuration
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
- Uvicorn

## Project Structure

```text
shortlink-api/
├── app/
│   ├── models/
│   │   └── link.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── .env.example
├── .gitignore
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

The application currently creates the required database tables automatically when it starts.

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
  "created_at": "2026-09-14T12:00:00"
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

## Short Code Generation

Short codes are generated using Python's `secrets` module.

Before storing a new link, the API checks whether the generated short code already exists. If a collision is detected, another code is generated, with a limited number of attempts.

The PostgreSQL database also enforces a unique constraint on short codes.

## Roadmap

The current version implements the core URL-shortening functionality.

Planned improvements:

- Database migrations with Alembic
- Automated tests with pytest
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