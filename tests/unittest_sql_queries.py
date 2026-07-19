import unittest
import pandas as pd

from src.database.sql_queries import (
    df,
    df1,
    df2,
    df3,
    df4
)


class TestDatabaseQueries(unittest.TestCase):

 

    def test_dataframe_not_empty(self):

        self.assertFalse(df.empty)

    def test_required_columns_exist(self):

        required_columns = [
            "time",
            "latitude",
            "longitude",
            "depth",
            "magnitude",
            "area_name",
            "source"
        ]

        for col in required_columns:
            self.assertIn(col, df.columns)

    

    def test_query1_not_empty(self):

        self.assertFalse(df1.empty)

    def test_query1_columns(self):

        columns = [
            "month",
            "area_name",
            "total_earthquakes"
        ]

        for col in columns:
            self.assertIn(col, df1.columns)

    

    def test_query2_not_empty(self):

        self.assertFalse(df2.empty)

    def test_query2_columns(self):

        columns = [
            "area_name",
            "source",
            "avg_magnitude"
        ]

        for col in columns:
            self.assertIn(col, df2.columns)



    def test_query3_not_empty(self):

        self.assertFalse(df3.empty)

    def test_query3_max_rows(self):

        self.assertLessEqual(
            len(df3),
            10
        )

  

    def test_query4_not_empty(self):

        self.assertFalse(df4.empty)

    def test_query4_columns(self):

        columns = [
            "area_name",
            "max_depth",
            "min_depth"
        ]

        for col in columns:
            self.assertIn(col, df4.columns)

   

    def test_depth_values_valid(self):
        """بررسی max_depth >= min_depth"""

        self.assertTrue(
            (df4["max_depth"] >= df4["min_depth"]).all()
        )

    def test_magnitude_positive(self):
        """بررسی مثبت بودن magnitude"""

        self.assertTrue(
            (df["magnitude"] >= 0).all()
        )


if __name__ == "__main__":
    unittest.main()