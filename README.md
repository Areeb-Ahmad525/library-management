# Library Management System

A small Python application for managing books, members, and loans in a library. The project follows a layered architecture with a CLI front end, service layer, repository layer, and SQLAlchemy-based persistence.

## Features

- Add, list, search, update, and delete books
- Register, list, search, update, and delete members
- Issue and return books to members
- Prevent duplicate active loans and validate common input rules
- Use PostgreSQL with SQLAlchemy and Alembic migrations

## Project structure

- src/cli: interactive terminal interface
- src/services: business rules and validation
- src/repositories: persistence and data access
- src/database: ORM models, session management, and engine setup
- src/config: environment-based application settings
- tests: regression tests for repositories and services

## Requirements

- Python 3.13+
- PostgreSQL (or Docker Compose for local development)
- Optional: uv for dependency and environment management

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:
   - `uv sync --extra dev`
3. Create a `.env` file with the database settings you want to use, for example:
   - `DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/library_db`
4. Start PostgreSQL locally or with Docker Compose.

## Run with Docker Compose

If you want to run the app and database together:

```bash
docker compose up --build
```

The Compose setup starts:
- the application container
- a PostgreSQL container on port 5433

## Run the CLI

From the project root:

```bash
uv run python src/main.py
```

## Run tests

```bash
uv run python -m unittest discover -s tests -v
```

## Database migrations

Alembic is configured for schema migrations. To create or apply migrations, use the usual Alembic commands from the project root.
