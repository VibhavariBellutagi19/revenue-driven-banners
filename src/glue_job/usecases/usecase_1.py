from common import read_utils
from pyspark.sql import DataFrame, SparkSession
from abstract_usecase import UseCase
from log.custom_logger import CustomLog

NUM_OF_BANNERS = 10

QUERY_FILE_NAME = "usecase_1_query.sql"


class UseCase1(UseCase, CustomLog):
    """
    UseCase1 - x >= 10 - Show the Top 10 banners based on revenue within that campaign
    """

    def compute_use_case(self, spark: SparkSession) -> DataFrame:
        """
        Computes the use case 1 scenario - x >= 10 - Show the Top 10 banners based on revenue within that campaign
        :param spark: spark session
        :return: top 10 banner id on revenue within the campaign id
        """
        query = read_utils.read_sql_query_from_file(QUERY_FILE_NAME).format(NUM_OF_BANNERS)
        self.log_info(f"Executing usecase_1 query - {self.query}")

        result_df = spark.sql(query)
        return result_df
