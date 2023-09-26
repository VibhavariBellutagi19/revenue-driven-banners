import importlib.resources

RESOURCE_PACKAGE = 'resources'


def read_sql_query_from_file(query_file_path: str) -> str:
    query = read_file(query_file_path)

    return query


def read_file(query_file):
    return importlib.resources.read_text(RESOURCE_PACKAGE, query_file)


def retrieve_from_s3(spark, path, input_format, schema):
    return spark.read.format(input_format).schema(schema).load(path)
