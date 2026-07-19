import unittest
import pandas as pd
import numpy as np
import re


from src.processing.all_csv import (
    df_usgs,
    df_geofon,
    df_messy,
    df_emsc,
    df_combined,
    table1,
    table2,
    table3,
    convert_type,
    mag_to_float,
    depth_clean
)

class TestEarthquakeCleaning(unittest.TestCase):

    def test_dataframes_not_empty(self):
        

        self.assertFalse(df_usgs.empty)
        self.assertFalse(df_geofon.empty)
        self.assertFalse(df_messy.empty)
        self.assertFalse(df_emsc.empty)
        self.assertFalse(df_combined.empty)

    def test_combined_shape(self):
        
        total_rows = (
            len(df_usgs) +
            len(df_geofon) +
            len(df_messy) +
            len(df_emsc)
        )

        self.assertEqual(
            len(df_combined),
            total_rows
        )

    def test_required_columns_exist(self):
        
        required_columns = [
            "time",
            "latitude",
            "longitude",
            "depth",
            "magnitude",
            "place",
            "month",
            "category",
            "area_name",
            "source"
        ]

        for col in required_columns:
            self.assertIn(
                col,
                df_combined.columns
            )

    
    def test_convert_type_iso(self):
        value = "2025-09-15T12:45:30.123Z"

        result = convert_type(value)

        self.assertIsInstance(
            result,
            pd.Timestamp
        )

    def test_convert_type_month_name(self):
        value = "Sep 17, 2025, 14:10:05"

        result = convert_type(value)

        self.assertIsInstance(
            result,
            pd.Timestamp
        )

    def test_convert_type_am_pm(self):
        value = "2025-09-27 03:30 PM"

        result = convert_type(value)

        self.assertIsInstance(
            result,
            pd.Timestamp
        )

    def test_convert_type_slash(self):
        value = "22/09/2025 11:05:21"

        result = convert_type(value)

        self.assertIsInstance(
            result,
            pd.Timestamp
        )

    def test_regex_iso_match(self):
        
        pattern = r"\d{4}-\d{2}-\d{2}T"

        value = "2025-09-15T12:45:30.123Z"

        self.assertIsNotNone(
            re.match(pattern, value)
        )

    def test_regex_month_match(self):
        pattern = r"[A-Za-z]{3}\s\d{1,2},\s\d{4}"

        value = "Sep 17, 2025, 14:10:05"

        self.assertIsNotNone(
            re.match(pattern, value)
        )

    def test_regex_am_pm_match(self):
        

        pattern = r"\d{4}-\d{2}-\d{2}\s"

        value = "2025-09-27 03:30 PM"

        self.assertIsNotNone(
            re.match(pattern, value)
        )

    def test_regex_slash_match(self):
       
        pattern = r"\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}"

        value = "22/09/2025 11:05:21"

        self.assertIsNotNone(
            re.match(pattern, value)
        )

   
    def test_mag_to_float_words(self):
       
        self.assertEqual(
            mag_to_float("five point six"),
            5.6
        )

    def test_mag_to_float_numeric(self):
        
        self.assertEqual(
            mag_to_float("4.5"),
            4.5
        )

    def test_mag_to_float_invalid(self):
        
        result = mag_to_float("abc")

        self.assertTrue(
            np.isnan(result)
        )

    def test_depth_clean_km(self):
        self.assertEqual(
            depth_clean("10 km"),
            10.0
        )

    def test_depth_clean_miles(self):
        
        result = depth_clean("1 miles")

        self.assertAlmostEqual(
            result,
            1.6093,
            places=3
        )

    def test_depth_clean_meters(self):
        
        result = depth_clean("500 meters")

        self.assertEqual(
            result,
            0.5
        )

    def test_depth_clean_negative(self):
        
        self.assertEqual(
            depth_clean(-20),
            20.0
        )

    def test_category_values(self):
        
        valid_categories = {
            "Weak",
            "Average",
            "Severe"
        }
        categories = set(
            df_combined["category"].unique()
        )
        self.assertTrue(
            categories.issubset(valid_categories)
        )


    def test_source_column_exists(self):
        

        self.assertIn(
            "source",
            df_combined.columns
        )
    def test_source_values(self):
        
        valid_sources = {
            "JAPAN_USGS",
            "JAPAN_GEOFON",
            "JAPAN_EMSC",
            "japan_messy_earthquakes"
        }

        sources = set(
            df_combined["source"].unique()
        )

        self.assertTrue(
            sources.issubset(valid_sources)
        )

    def test_table1_not_empty(self):
        

        self.assertFalse(
            table1.empty
        )

    def test_table2_not_empty(self):
        

        self.assertFalse(
            table2.empty
        )

    def test_table3_not_empty(self):
        

        self.assertFalse(
            table3.empty
        )

    def test_depth_positive(self):
    
        self.assertTrue(
            (df_combined["depth"] >= 0).all()
        )

    def test_latitude_range(self):
        
        self.assertTrue(
            df_combined["latitude"]
            .between(-90, 90)
            .all()
        )

    def test_longitude_range(self):
        
        self.assertTrue(
            df_combined["longitude"]
            .between(-180, 180)
            .all()
        )

    def test_index_starts_from_one(self):
        
        self.assertEqual(
            df_combined.index[0],
            1
        )

