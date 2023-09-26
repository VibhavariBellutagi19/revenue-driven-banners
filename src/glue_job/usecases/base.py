from pyspark.sql import SparkSession

from common import read_utils
from log.custom_logger import CustomLog

QUERY_FILE_NAME = "base_query.sql"


class Base(CustomLog):
    query = read_utils.read_sql_query_from_file(QUERY_FILE_NAME)

    def get_number_of_banners(self, spark: SparkSession):
        self.log_info(f"Executing base query - {self.query}")
        return spark.sql(self.query)
