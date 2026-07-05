import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")


class Settings:
    """Application settings loaded from environment variables."""

    DATABASE_URL: Final[str] = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5433/library_db",
    )

    POSTGRES_DB: Final[str] = os.getenv("POSTGRES_DB", "library_db")
    POSTGRES_USER: Final[str] = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: Final[str] = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: Final[str] = os.getenv("POSTGRES_PORT", "5433")


settings = Settings()
