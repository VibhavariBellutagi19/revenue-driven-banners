resource "aws_glue_connection" "glue_connection" {

  connection_type = "NETWORK"

  connection_properties = {}

  name        = "revenue-driven-banner-2023"
  description = "Glue connection used for tha-vibhavari-bellutagi-assignment"

  physical_connection_requirements {
    security_group_id_list = [local.vars.security_group]
    subnet_id              = local.vars.subnet_id
    availability_zone      = local.vars.availability_zone_id
  }
  
}

resource "aws_glue_catalog_database" "aws_glue_catalog_database" {
  name         = "banners"
  description  = "Glue database used for tha-vibhavari-bellutagi-assignment"
  location_uri = "s3://${aws_s3_bucket.s3_bucket.id}/data"
}

resource "aws_glue_job" "compute_banners" {
  name                      = "compute-banners"
  description               = "Glue job for computing the banner id based on its performance"
  role_arn                  = aws_iam_role.glue_job_role.arn
  glue_version              = "4.0"
  command {
    name            = "glueetl"
    script_location = "s3://${aws_s3_bucket.s3_bucket.id}/code/glue/main.py"
    python_version  = "3"
  }
  default_arguments = {
    "--enable-glue-datacatalog"               = ""
    "--additional-python-modules"             = "s3://${aws_s3_bucket.s3_bucket.id}/${aws_s3_object.s3_object_glue_common.id}"
    "--extra-py-files"                        = "s3://${aws_s3_bucket.s3_bucket.id}/${aws_s3_object.s3_object_glue_common.id}"
    "--conf"                                  = "spark.sql.sources.partitionOverwriteMode=dynamic --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension"
    "--bucket_name"                           =  aws_s3_bucket.s3_bucket.id
    "--dataset_id"                           =  "dataset-1"
  }
  worker_type               = "G.2X"
  number_of_workers         = 2
  connections               = [aws_glue_connection.glue_connection.name]
  timeout                   = 2880
  execution_property {
    max_concurrent_runs = 1
  }
}