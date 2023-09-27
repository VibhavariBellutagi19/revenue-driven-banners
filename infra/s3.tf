locals {
  src_path = "${path.module}/../src"
  target_path = "${path.module}/../target"
  glue_main = local.vars["glue_main"]
  version = file("${path.module}/../VERSION")
  glue_common = "${local.vars.glue_common}-${local.version}-py3-none-any.whl"
  lambdas = toset([
    "${local.vars["push_to_dynamodb"]}_${local.version}.zip"
  ])
}

resource "aws_s3_bucket" "s3_bucket" {
  bucket = local.vars["bucket_name"]
}

# Uploads the lambda source code to s3
resource "aws_s3_object" "s3_object_lambda" {
  bucket         = aws_s3_bucket.s3_bucket.id
  for_each       = local.lambdas
  key            = "code/lambdas/${each.value}"
  source         = "${local.target_path}/${each.value}"
  source_hash    = filemd5("${local.target_path}/${each.value}")
}

# Uploads glue source code to s3
resource "aws_s3_object" "s3_object_glue" {
  bucket = aws_s3_bucket.s3_bucket.id
  key = "code/glue/${local.glue_main}"
  source = "${local.src_path}/glue_job/${local.glue_main}"
  source_hash = filemd5("${local.src_path}/glue_job/${local.glue_main}")
}

# Uploads glue common code to s3
resource "aws_s3_object" "s3_object_glue_common" {
  bucket = aws_s3_bucket.s3_bucket.id
  key = "code/glue/${local.glue_common}"
  source = "${local.target_path}/${local.glue_common}"
  source_hash = filemd5("${local.target_path}/${local.glue_common}")
}