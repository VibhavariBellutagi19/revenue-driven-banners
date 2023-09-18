import pytest
from pyspark import Row
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def test_data_usecase_1(spark: SparkSession):
    conversions_data = [
        Row(conversion_id=2000, click_id=100013, revenue=1.173893),
        Row(conversion_id=2001, click_id=100014, revenue=1.1734),
        Row(conversion_id=2002, click_id=100015, revenue=0.145234),
        Row(conversion_id=2003, click_id=100016, revenue=1.134242),
        Row(conversion_id=2004, click_id=100017, revenue=1.012932),
        Row(conversion_id=2005, click_id=100018, revenue=0.352413),
        Row(conversion_id=2006, click_id=100019, revenue=5.342342),
        Row(conversion_id=2007, click_id=100020, revenue=1.142528),
        Row(conversion_id=2008, click_id=100021, revenue=1.02497),
        Row(conversion_id=2009, click_id=100022, revenue=0.631612),
        Row(conversion_id=2010, click_id=100023, revenue=1.08564)
    ]

    # Define schema for clicks
    clicks_data = [
        Row(click_id=100013, banner_id=328, campaign_id=1),
        Row(click_id=100014, banner_id=321, campaign_id=1),
        Row(click_id=100015, banner_id=123, campaign_id=1),
        Row(click_id=100016, banner_id=345, campaign_id=1),
        Row(click_id=100017, banner_id=432, campaign_id=1),
        Row(click_id=100018, banner_id=567, campaign_id=1),
        Row(click_id=100019, banner_id=765, campaign_id=1),
        Row(click_id=100020, banner_id=234, campaign_id=1),
        Row(click_id=100021, banner_id=430, campaign_id=1),
        Row(click_id=100022, banner_id=465, campaign_id=1),
        Row(click_id=100023, banner_id=465, campaign_id=1),
        Row(click_id=100001, banner_id=465, campaign_id=1)
    ]

    # Create DataFrames from sample data
    df_conversions = spark.createDataFrame(conversions_data)
    df_clicks = spark.createDataFrame(clicks_data)
    