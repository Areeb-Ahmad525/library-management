import unittest

from fastapi.testclient import TestClient

from src.api.app import create_app
from src.database.models import Book
from src.database.session import SessionLocal


class FastAPITests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(create_app())
        self.db = SessionLocal()
        self.db.query(Book).filter(Book.title.in_(["The Hobbit", "Dune"])).delete(synchronize_session=False)
        self.db.commit()
        self.db.add_all(
            [
                Book(title="The Hobbit", author="J.R.R. Tolkien"),
                Book(title="Dune", author="Frank Herbert"),
            ]
        )
        self.db.commit()

    def tearDown(self) -> None:
        self.db.query(Book).filter(Book.title.in_(["The Hobbit", "Dune"])).delete(synchronize_session=False)
        self.db.commit()
        self.db.close()

    def test_list_books_endpoint(self) -> None:
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertGreaterEqual(len(payload), 2)
        self.assertTrue(any(item["title"] == "The Hobbit" for item in payload))

    def test_search_books_endpoint(self) -> None:
        response = self.client.get("/books/search", params={"title": "hobbit"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["title"], "The Hobbit")


if __name__ == "__main__":
    unittest.main()
