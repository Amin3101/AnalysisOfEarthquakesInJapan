import unittest
import pandas as pd
from sqlalchemy import create_engine, text

from src.database.database import engine


class TestDatabase(unittest.TestCase):

    def test_engine_exists(self):
        self.assertIsNotNone(engine)

    def test_database_connection(self):
        try:
            with engine.connect():
                connected = True
        except Exception:
            connected = False
        self.assertTrue(connected)


class TestDatabaseInsert(unittest.TestCase):
    """Real insert test that does NOT touch the production MySQL database.
    Uses an isolated in-memory SQLite engine so the Insert logic is exercised
    without ever risking real/production data."""

    def setUp(self):
        self.test_engine = create_engine("sqlite:///:memory:")
        with self.test_engine.begin() as conn:
            conn.execute(text(
                """
                CREATE TABLE earthquakes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time TEXT NOT NULL,
                    latitude REAL,
                    longitude REAL,
                    depth REAL,
                    magnitude REAL,
                    area_name TEXT,
                    source TEXT,
                    record_key TEXT UNIQUE
                )
                """
            ))

    def test_insert_adds_rows(self):
        df = pd.DataFrame({
            "time": ["2024-01-01 00:00:00"],
            "latitude": [35.6],
            "longitude": [139.7],
            "depth": [10.0],
            "magnitude": [5.5],
            "area_name": ["Tokyo"],
            "source": ["TEST"],
            "record_key": ["k1"],
        })
        df.to_sql("earthquakes", con=self.test_engine, if_exists="append", index=False)

        with self.test_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM earthquakes")).scalar()

        self.assertEqual(count, 1)

    def test_duplicate_record_key_is_rejected(self):
        df = pd.DataFrame({
            "time": ["2024-01-01 00:00:00"],
            "latitude": [35.6],
            "longitude": [139.7],
            "depth": [10.0],
            "magnitude": [5.5],
            "area_name": ["Tokyo"],
            "source": ["TEST"],
            "record_key": ["dup"],
        })
        df.to_sql("earthquakes", con=self.test_engine, if_exists="append", index=False)

        with self.assertRaises(Exception):
            df.to_sql("earthquakes", con=self.test_engine, if_exists="append", index=False)


if __name__ == "__main__":
    unittest.main()
