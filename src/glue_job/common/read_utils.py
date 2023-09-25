def read_sql_query_from_file(query_file_path: str) -> str:
    with open(query_file_path, encoding="utf-8") as query_file:
        query = query_file.read()

    return query


def retrieve_from_s3(spark, path, input_format, schema):
    return spark.read.format(input_format).schema(schema).load(path)
