from sqlalchemy import text

from database.session import SessionLocal


def main():
    db = SessionLocal()

    result = db.execute(text("SELECT version();"))

    print(result.scalar())

    db.close()


if __name__ == "__main__":
    main()