import unittest

import pytest
from pyspark.sql import SparkSession

from glue_job.usecases.base import ActionDataFrames
from glue_job.usecases.usecase_3 import UseCase3
from src.glue_job.usecases.usecase_2 import UseCase2
from src.glue_job.usecases.usecase_1 import UseCase1
from test_glue_job import TEST_ROOT


class TestComputeUseCases(unittest.TestCase):
    """
    Class for testing compute_use_cases
    """

    def get_dataframe(self, path):
        return self.spark. \
            read. \
            format("csv"). \
            option("inferSchema", True). \
            option("header", True).load(path)

    def setUp(self):
        self.spark = SparkSession.builder.master("local[2]") \
            .appName("test application") \
            .config("spark.ui.enabled", "false") \
            .getOrCreate()
        self.clicks_df = self.get_dataframe(f"{TEST_ROOT}/resources/test_clicks.csv")
        self.conversions_df = self.get_dataframe(f"{TEST_ROOT}/resources/test_conversions.csv")

    def tearDown(self) -> None:
        self.spark.stop()

    def test_compute_use_case_1(self):
        """
        test when the usecase_1 = x >= 10 -
        Show the Top 10 banners based on revenue within that campaign
        :return:
        """
        campaign_id = 1
        test_action_dataframes = ActionDataFrames(
            clicks_df=self.clicks_df,
            conversions_df=self.conversions_df
        )
        test_usecase_1 = UseCase1(campaign_id)
        result = test_usecase_1.compute_use_case(self.spark, test_action_dataframes)
        expected_len = 10

        assert result.count() == expected_len

    def test_compute_use_case_2(self):
        """
        test when the use case 2 - x in range(5,10) -
        Show the Top x banners based on revenue within that campaign
        :return:
        """
        campaign_id = 2
        number_of_banners = 6

        test_action_dataframes = ActionDataFrames(
            clicks_df=self.clicks_df,
            conversions_df=self.conversions_df
        )
        test_usecase_2 = UseCase2(campaign_id, number_of_banners)
        result = test_usecase_2.compute_use_case(self.spark, test_action_dataframes)
        expected_len = 6

        assert result.count() == expected_len

    def test_compute_use_case_3(self):
        """
        test when the use_case 3 - x in range of 1-5 - Show the top 5 banners based on clicks.
        If the number of banners with clicks is less than 5 within that campaign,
        then you should add random banners to make up a collection of 5 unique banners.
        :return:
        """
        campaign_id = 3

        test_action_dataframes = ActionDataFrames(
            clicks_df=self.clicks_df,
            conversions_df=self.conversions_df
        )
        test_usecase_3 = UseCase3(campaign_id)
        result = test_usecase_3.compute_use_case(self.spark, test_action_dataframes)
        expected_len = 6

        assert result.count() == expected_len

