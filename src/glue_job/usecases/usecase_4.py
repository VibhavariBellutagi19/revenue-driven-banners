from pyspark.sql import DataFrame, SparkSession

from .. import GLUE_ROOT
from ..common import read_utils
from ..usecases.abstract_usecase import UseCase

QUERY_FILE_PATH = f"{GLUE_ROOT}/resources/usecase_4_query.sql"


class UseCase4(UseCase):
    """
    UseCase1 - x >= 10 - Show the Top 10 banners based on revenue within that campaign
    """

    def __init__(self, campaign_id: int):
        self.campaign_id = campaign_id

    def compute_use_case(self, spark: SparkSession) -> DataFrame:
        """
        Computes the use case 1 scenario - x >= 10 - Show the Top 10 banners based on revenue within that campaign
        :param spark: spark session
        :return: top 10 banner id on revenue within the campaign id
        """
        query = read_utils.read_sql_query_from_file(QUERY_FILE_PATH.format())

        result_df = spark.sql(query)
        return result_df
