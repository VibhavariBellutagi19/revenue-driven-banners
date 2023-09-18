from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql import DataFrame, SparkSession

from ..usecases.base import UseCase, ActionDataFrames


class UseCase1(UseCase):
    """
    UseCase1 - x >= 10 - Show the Top 10 banners based on revenue within that campaign
    """

    def __init__(self, campaign_id: int):
        self.campaign_id = campaign_id

    def compute_use_case(self, spark: SparkSession, dataframes: ActionDataFrames) -> DataFrame:
        """
        Computes the use case 1 scenario - x >= 10 - Show the Top 10 banners based on revenue within that campaign
        :param dataframes: input dataframes for computing use_case
        :param spark: spark session
        :return: top 10 banner id on revenue within the campaign id
        """
        click_df = dataframes.clicks_df
        conversions_df = dataframes.conversions_df

        window_spec = Window.partitionBy("campaign_id").orderBy(F.desc("revenue"))

        # Joining the two dataframes
        joined_df = conversions_df.alias('cn').join(click_df.alias('cl'),
                                                    conversions_df.click_id == click_df.click_id,
                                                    "inner")

        # Adding the dense rank column
        with_rank_df = joined_df.withColumn("rnk", F.dense_rank().over(window_spec))

        # Filtering based on campaign_id and rank
        result_df = with_rank_df.filter((with_rank_df.campaign_id == self.campaign_id)
                                        & (with_rank_df.rnk <= 10)).\
            select("banner_id", "campaign_id").distinct()
        return result_df
