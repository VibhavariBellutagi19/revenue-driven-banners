from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import count, col, rand

from ..usecases.base import UseCase, ActionDataFrames


class UseCase3(UseCase):
    """
    class for Usecase - 3
    """

    def __init__(self, campaign_id: int, number_of_banners: int):
        self.campaign_id = campaign_id

    def compute_use_case(self, spark: SparkSession, dataframes: ActionDataFrames) -> DataFrame:
        """
        Computes the use case 13 scenario,
        x in range of 1-5 - Show the top 5 banners based on clicks. If the number of banners with clicks is less than 5
        within that campaign, then you should add random banners to make up a collection of 5 unique banners.
        :param dataframes: input dataframes needed for computing the usecases.
        :param spark: spark session
        :return: top 10 banner id on revenue within the campaign id
        """
        clicks_df = dataframes.clicks_df.filter(dataframes.clicks_df["campaign_id"] == self.campaign_id)

        # Group by banner_id and count the number of clicks
        banner_clicks = clicks_df.groupBy("banner_id").agg(count("click_id").alias("num_clicks"))

        top_banners = banner_clicks.orderBy(col("num_clicks").desc()).limit(5)

        num_top_banners = top_banners.count()

        if num_top_banners < 5:
            # Exclude the banners already in the top list
            remaining_banners = clicks_df.join(top_banners, on="banner_id", how="left_anti")
            distinct_remaining_banners = remaining_banners.groupBy("banner_id").count()
            additional_banners = distinct_remaining_banners.orderBy(rand()).limit(5 - num_top_banners)
            final_top_banners = top_banners.union(additional_banners.drop("count"))
        else:
            final_top_banners = top_banners

        return final_top_banners

