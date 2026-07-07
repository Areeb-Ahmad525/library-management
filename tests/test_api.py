import unittest

from fastapi.testclient import TestClient

from src.api.app import create_app
from src.database.models import Book, Member, Loan
from src.database.base import Base


class FastAPITests(unittest.TestCase):
    def setUp(self) -> None:
        from sqlalchemy.orm import Session
        from src.database.session import engine
        from src.api.app import get_db

        self.connection = engine.connect()
        self.transaction = self.connection.begin()
        self.session = Session(
            bind=self.connection, join_transaction_mode="create_savepoint"
        )
        
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())

        app = create_app()
        app.dependency_overrides[get_db] = lambda: self.session
        self.client = TestClient(app)

        self.session.add_all(
            [
                Book(title="The Hobbit", author="J.R.R. Tolkien"),
                Book(title="Dune", author="Frank Herbert"),
            ]
        )
        self.session.flush()

    def tearDown(self) -> None:
        self.client.close()
        self.session.close()
        self.transaction.rollback()
        self.connection.close()

    @classmethod
    def tearDownClass(cls) -> None:
        from src.database.session import engine
        engine.dispose()

    def test_list_books_endpoint(self) -> None:
        """Verify the /books endpoint successfully retrieves the list of books."""
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertGreaterEqual(len(payload), 2)
        self.assertTrue(any(item["title"] == "The Hobbit" for item in payload))

    def test_search_books_endpoint(self) -> None:
        """Verify the /books/search endpoint accurately filters books by query parameters."""
        response = self.client.get("/books/search", params={"title": "hobbit"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["title"], "The Hobbit")


if __name__ == "__main__":
    unittest.main()
