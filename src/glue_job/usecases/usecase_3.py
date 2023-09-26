from pyspark.sql import DataFrame, SparkSession

from common import read_utils
from abstract_usecase import UseCase
from log.custom_logger import CustomLog

TOP_X = 5

QUERY_FILE = "usecase_3_query.sql"


class UseCase3(UseCase, CustomLog):
    """
    class for Usecase - 3
    """

    def __init__(self, number_of_banners: int):
        self.number_of_banners = number_of_banners

    def compute_use_case(self, spark: SparkSession) -> DataFrame:
        """
        Computes the use case 3 scenario
        :param spark: spark session
        :return: top 10 banner id on revenue within the campaign id
        """
        additional_banners = TOP_X - self.number_of_banners
        query = read_utils.read_sql_query_from_file(QUERY_FILE).format(self.number_of_banners, additional_banners)
        self.log_info(f"Executing usecase_3 query - {self.query}")

        result_df = spark.sql(query)
        return result_df
