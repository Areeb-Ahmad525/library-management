import sys
import logging
from pathlib import Path

# Ensure src module is in the path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.database.session import SessionLocal  # noqa: E402
from src.database.models import Book, Member, Loan  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_data():
    db = SessionLocal()
    try:
        logger.info("Clearing existing database tables...")
        db.query(Loan).delete()
        db.query(Book).delete()
        db.query(Member).delete()
        db.commit()

        logger.info("Seeding database with mock data...")

        # Create Books
        books = [
            Book(title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams"),
            Book(title="Dune", author="Frank Herbert"),
            Book(title="1984", author="George Orwell"),
            Book(title="Fahrenheit 451", author="Ray Bradbury"),
            Book(title="Foundation", author="Isaac Asimov"),
            Book(title="Brave New World", author="Aldous Huxley"),
        ]
        db.add_all(books)
        db.commit()

        # Create Members
        members = [
            Member(name="Alice Smith", email="alice@example.com"),
            Member(name="Bob Johnson", email="bob@example.com"),
            Member(name="Charlie Brown", email="charlie@example.com"),
        ]
        db.add_all(members)
        db.commit()

        # Create an active loan
        loan = Loan(book_id=books[0].id, member_id=members[0].id)
        db.add(loan)
        db.commit()

        logger.info("Successfully seeded database!")

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to seed database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
