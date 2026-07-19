import unittest
import pandas as pd

from src.processing.geometry_engine import GeometryEngine


class TestGeometryEngine(unittest.TestCase):

    def setUp(self):

        self.geo = GeometryEngine()

        self.df = pd.DataFrame({
            'latitude': [35.6, 38.3, 20.0],
            'longitude': [139.7, 142.4, 110.0],
            'depth': [10.5, 24.0, 5.0]
        })

    # =========================================
    #           validate_input
    # =========================================

    def test_validate_input_valid(self):

        result = self.geo._validate_input(self.df)

        self.assertTrue(result)

    def test_validate_input_empty(self):

        empty_df = pd.DataFrame()

        result = self.geo._validate_input(empty_df)

        self.assertFalse(result)

    def test_validate_input_missing_column(self):

        bad_df = pd.DataFrame({
            'latitude': [35.0],
            'longitude': [140.0]
        })

        result = self.geo._validate_input(bad_df)

        self.assertFalse(result)

    # =========================================
    #           calculate_metrics
    # =========================================

    def test_calculate_metrics_add_columns(self):

        result = self.geo.calculate_metrics(self.df)

        self.assertIn('dist_to_ref_km', result.columns)
        self.assertIn('hypocenter_dist_km', result.columns)
        self.assertIn('is_in_japan_bounds', result.columns)

    def test_distance_positive(self):

        result = self.geo.calculate_metrics(self.df)

        self.assertTrue(
            (result['dist_to_ref_km'] >= 0).all()
        )

    def test_hypocenter_distance_positive(self):

        result = self.geo.calculate_metrics(self.df)

        self.assertTrue(
            (result['hypocenter_dist_km'] >= 0).all()
        )

    def test_japan_bounds(self):

        result = self.geo.calculate_metrics(self.df)

        self.assertEqual(
            result['is_in_japan_bounds'].tolist(),
            [True, True, False]
        )

    def test_invalid_dataframe_returns_same(self):

        bad_df = pd.DataFrame()

        result = self.geo.calculate_metrics(bad_df)

        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()