import logging


def configure_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
