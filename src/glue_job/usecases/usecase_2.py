from pyspark.sql import DataFrame, SparkSession

from common import read_utils
from .abstract_usecase import UseCase
from log.custom_logger import CustomLog

QUERY_FILE = "usecase_2_query.sql"


class UseCase2(UseCase, CustomLog):
    """
    UseCase2 - class for use case 2
    """

    def __init__(self, num_of_banners: int):
        self.num_of_banners = num_of_banners

    def compute_use_case(self, spark: SparkSession) -> DataFrame:
        """
        Computes the use case 2 - x in range(5,10) -
        Show the Top x banners based on revenue within that campaign
        :param spark: spark session
        :return: top x banner id on revenue within the campaign id
        """
        query = read_utils.read_sql_query_from_file(QUERY_FILE).format(self.num_of_banners)
        self.log_info(f"Executing usecase_2 query - {self.query}")

        result_df = spark.sql(query)
        return result_df
