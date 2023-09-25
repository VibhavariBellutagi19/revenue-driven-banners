import sys

from awsglue.context import GlueContext  # pylint: disable=import-error
from awsglue.job import Job  # pylint: disable=import-error
from awsglue.utils import getResolvedOptions  # pylint: disable=import-error
from pyspark.context import SparkContext
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType

from glue_job.common.read_utils import retrieve_from_s3
from glue_job.common.write_utils import save_to_s3_parquet
from glue_job.usecases.base import Base
from glue_job.usecases.factory import UseCaseFactory

FORMAT = ".csv"

CLICK_SCHEMA = StructType([
    StructField("click_id", IntegerType(), True),
    StructField("banner_id", IntegerType(), True),
    StructField("campaign_id", IntegerType(), True)
])

IMPRESSIONS_SCHEMA = StructType([
    StructField("click_id", IntegerType(), True),
    StructField("banner_id", IntegerType(), True)
])

CONVERSIONS_SCHEMA = StructType([
    StructField("conversion_id", IntegerType(), True),
    StructField("click_id", IntegerType(), True),
    StructField("revenue", FloatType(), True),
])


class S3PathBuilder:
    def __init__(self, bucket_name, dataset_id):
        self.bucket_name = bucket_name
        self.dataset_id = dataset_id

    def build_path(self, file_name):
        return f"s3://{self.bucket_name}/raw/{self.dataset_id}/{file_name}"


def main():
    query_mapping = ['JOB_NAME', 'dataset_id', 'bucket_name']

    args = getResolvedOptions(sys.argv,
                              query_mapping)

    glue_context = GlueContext(SparkContext.getOrCreate())
    job = Job(glue_context)
    job.init(args["JOB_NAME"], args)
    bucket_name = args['bucket_name']
    dataset_id = args['dataset_id']
    banners = "banners-campaigns"

    spark = glue_context.sparkSession \
        .builder \
        .getOrCreate()

    path_builder = S3PathBuilder(bucket_name, dataset_id)

    clicks_df = retrieve_from_s3(spark, path_builder.build_path('clicks.csv'), FORMAT, CLICK_SCHEMA)
    conversions_df = retrieve_from_s3(spark, path_builder.build_path('conversions.csv'), FORMAT, CONVERSIONS_SCHEMA)
    impressions_df = retrieve_from_s3(spark, path_builder.build_path('impressions.csv'), FORMAT, IMPRESSIONS_SCHEMA)

    clicks_df.createOrReplaceTempView("clicks")
    conversions_df.createOrReplaceTempView("conversions")
    impressions_df.createOrReplaceTempView("impressions")

    base = Base()
    number_of_banners = base.get_number_of_banners(spark)
    usecase = UseCaseFactory.get_usecase(number_of_banners)
    computed_df = usecase.compute_use_case(spark)

    computed_df = computed_df.withColumn("dataset_id", dataset_id)

    save_to_s3_parquet(computed_df, bucket_name, banners, usecase)


if __name__ == "__main__":
    main()
