import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

from src.processing.all_csv import df_combined


class TestEarthquakeVisualization(unittest.TestCase):

    def setUp(self):

        self.df = df_combined.copy()

        self.df['time'] = pd.to_datetime(
            self.df['time'],
            errors='coerce'
        )

    # ======================================
    #               Data Tests
    # ======================================

    def test_dataframe_not_empty(self):

        self.assertFalse(self.df.empty)

    def test_required_columns_exist(self):

        columns = [
            'area_name',
            'magnitude',
            'time',
            'depth',
            'latitude',
            'longitude',
            'category'
        ]

        for col in columns:
            self.assertIn(col, self.df.columns)

    def test_magnitude_numeric(self):

        self.assertTrue(
            np.issubdtype(
                self.df['magnitude'].dtype,
                np.number
            )
        )

    # ======================================
    #                Regex Tests
    # ======================================

    def test_time_regex_iso_format(self):

        value = "2025-09-15T12:45:30.123Z"

        pattern = r"\d{4}-\d{2}-\d{2}T"

        self.assertIsNotNone(
            re.match(pattern, value)
        )

    def test_area_name_string(self):

        self.assertTrue(
            self.df['area_name'].dtype == object
        )

    # ======================================
    #              Histogram Test
    # ======================================

    def test_histogram_creation(self):

        city = self.df['area_name'].unique()[0]

        data = self.df[
            self.df['area_name'] == city
        ]['magnitude']

        fig, ax = plt.subplots()

        try:
            ax.hist(data)

            success = True

        except Exception:
            success = False

        plt.close(fig)

        self.assertTrue(success)

    # ======================================
    #           Line Chart Test
    # ======================================

    def test_line_chart_creation(self):

        df_weekly = self.df.set_index('time').resample('W').agg({
            'magnitude': ['count', 'mean']
        })

        fig, ax = plt.subplots()

        try:
            ax.plot(df_weekly.index)

            success = True

        except Exception:
            success = False

        plt.close(fig)

        self.assertTrue(success)

    # ======================================
    #           Scatter Plot Test
    # ======================================

    def test_scatter_plot_creation(self):

        fig, ax = plt.subplots()

        try:
            ax.scatter(
                self.df['time'],
                self.df['depth']
            )

            success = True

        except Exception:
            success = False

        plt.close(fig)

        self.assertTrue(success)

    # ======================================
    #             Boxplot Test
    # ======================================

    def test_boxplot_creation(self):

        weak = self.df[
            self.df['category'] == 'Weak'
        ]['magnitude']

        average = self.df[
            self.df['category'] == 'Average'
        ]['magnitude']

        severe = self.df[
            self.df['category'] == 'Severe'
        ]['magnitude']

        fig, ax = plt.subplots()

        try:
            ax.boxplot([weak, average, severe])

            success = True

        except Exception:
            success = False

        plt.close(fig)

        self.assertTrue(success)
    # ======================================
    #           Heatmap Test
    # ======================================

    def test_heatmap_creation(self):
        """بررسی رسم heatmap"""

        fig, ax = plt.subplots()

        try:
            sns.kdeplot(
                data=self.df,
                x='longitude',
                y='latitude',
                fill=True
            )

            success = True

        except Exception:
            success = False

        plt.close(fig)

        self.assertTrue(success)

    # ======================================
    #           Value Tests
    # ======================================
    def test_depth_positive(self):

        self.assertTrue(
            (self.df['depth'] >= 0).all()
        )

    def test_category_values(self):

        valid = ['Weak', 'Average', 'Severe']

        for cat in self.df['category'].unique():
            self.assertIn(cat, valid)


