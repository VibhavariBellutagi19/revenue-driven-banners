from pyspark.sql import DataFrame, SparkSession

from .. import GLUE_ROOT
from ..common import read_utils
from ..usecases.abstract_usecase import UseCase

QUERY_FILE_PATH = f"{GLUE_ROOT}/resources/usecase_2_query.sql"


class UseCase2(UseCase):
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
        query = read_utils.read_sql_query_from_file(QUERY_FILE_PATH.format(self.num_of_banners))

        result_df = spark.sql(query)
        return result_df
