from log.custom_logger import CustomLog


def save_to_s3_parquet(df, bucket, db, table):
    custom_log = CustomLog()

    path = f"s3://{bucket}/output/{table}"
    custom_log.log_info(f"write the dataframe to the path - {path} ...")
    df.write. \
        format("parquet"). \
        partitionBy("dataset_id", "campaign_id"). \
        mode("overwrite"). \
        option("path", path). \
        saveAsTable(f"{db}.{table}")
