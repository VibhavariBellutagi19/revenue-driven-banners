from pyspark.sql import DataFrame, SparkSession

from .. import GLUE_ROOT
from ..common import read_utils
from ..usecases.abstract_usecase import UseCase

NUM_OF_BANNERS = 10

QUERY_FILE_PATH = f"{GLUE_ROOT}/resources/usecase_1_query.sql"


class UseCase1(UseCase):
    """
    UseCase1 - x >= 10 - Show the Top 10 banners based on revenue within that campaign
    """

    def compute_use_case(self, spark: SparkSession) -> DataFrame:
        """
        Computes the use case 1 scenario - x >= 10 - Show the Top 10 banners based on revenue within that campaign
        :param spark: spark session
        :return: top 10 banner id on revenue within the campaign id
        """
        query = read_utils.read_sql_query_from_file(QUERY_FILE_PATH.format(NUM_OF_BANNERS))

        result_df = spark.sql(query)
        return result_df
