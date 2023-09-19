import unittest

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, IntegerType, StructField, FloatType

from glue_job.usecases.abstract_usecase import ActionDataFrames
from glue_job.usecases.usecase_3 import UseCase3
from src.glue_job.usecases.usecase_1 import UseCase1
from src.glue_job.usecases.usecase_2 import UseCase2
from test_glue_job import TEST_ROOT


class TestComputeUseCases(unittest.TestCase):
    """
    Class for testing compute_use_cases
    """

    def get_dataframe(self, path, schema):
        return self.spark \
            .read \
            .format("csv") \
            .schema(schema) \
            .option("header", True).load(path)

    def setUp(self):
        self.spark = SparkSession.builder.master("local[2]") \
            .appName("test application") \
            .config("spark.ui.enabled", "false") \
            .getOrCreate()

        clicks_schema = StructType([
            StructField("click_id", IntegerType(), True),
            StructField("banner_id", IntegerType(), True),
            StructField("campaign_id", IntegerType(), True)
        ])

        conversions_schema = StructType([
            StructField("conversion_id", IntegerType(), True),
            StructField("click_id", IntegerType(), True),
            StructField("revenue", FloatType(), True),
        ])
        self.clicks_df = self.get_dataframe(f"{TEST_ROOT}/resources/test_clicks.csv", clicks_schema)
        self.conversions_df = self.get_dataframe(f"{TEST_ROOT}/resources/test_conversions.csv", conversions_schema)

    def tearDown(self) -> None:
        self.spark.stop()

    def test_compute_use_case_1(self):
        """
        test when the usecase_1 = x >= 10 -
        Show the Top 10 banners based on revenue within that campaign
        :return:
        """
        test_action_dataframes = ActionDataFrames(
            clicks_df=self.clicks_df,
            conversions_df=self.conversions_df
        )
        test_usecase_1 = UseCase1()
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

    def test_compute_use_case_3_when_num_of_banners_is_5(self, expected_len=None):
        """
        test when the use_case 3 - x - tests when num of banner is 5
        :return:
        """
        campaign_id = 3

        test_action_dataframes = ActionDataFrames(
            clicks_df=self.clicks_df
        )
        test_usecase_3 = UseCase3(campaign_id)
        result = test_usecase_3.compute_use_case(self.spark, test_action_dataframes)
        columns = ["banner_id", "campaign_id"]
        expected_len = 5

        assert list(result.columns) == columns
        assert result.count() == expected_len

    def test_compute_use_case_3_when_num_of_banners_is_less_than_5(self, expected_len=None):
        """
        test the use_case 3 - when num of banner is < 5
        :return:
        """
        campaign_id = 4

        test_action_dataframes = ActionDataFrames(
            clicks_df=self.clicks_df
        )
        test_usecase_3 = UseCase3(campaign_id)
        result = test_usecase_3.compute_use_case(self.spark, test_action_dataframes)
        columns = ["banner_id", "campaign_id"]
        expected_len = 4

        assert list(result.columns) == columns
        assert result.count() == expected_len
