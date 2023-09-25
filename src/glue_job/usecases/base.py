from pyspark.sql import DataFrame, SparkSession

from glue_job.common import read_utils

QUERY_FILE_PATH = "glue_job/resources/base_query.sql"


class Base:
    query = read_utils.read_sql_query_from_file(QUERY_FILE_PATH)

    def get_number_of_banners(self, spark: SparkSession):
        return spark.sql(self.query)
