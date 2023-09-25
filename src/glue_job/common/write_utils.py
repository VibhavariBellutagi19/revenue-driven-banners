def save_to_s3_parquet(df, bucket, db, table):
    path = f"s3://{bucket}/output/{table}"
    df.write. \
        format("parquet"). \
        partitionBy("dataset_id", "campaign_id"). \
        mode("overwrite"). \
        option("path", path). \
        saveAsTable(f"{db}.{table}")
