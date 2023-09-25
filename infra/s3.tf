locals {
  src_path = "${path.module}/../src"
  glue_main = local.vars["glue_main_path"]
  lambdas = toset([
    local.vars["trigger_lambda_path"],
    local.vars["trigger_lambda_path"],
    local.vars["trigger_lambda_path"]
  ])
}

resource "aws_s3_bucket" "s3_bucket" {
  bucket = local.vars["bucket_name"]
}

# Uploads the lambda source code to s3
resource "aws_s3_object" "s3_object_lambda" {
  bucket         = aws_s3_bucket.s3_bucket.id
  for_each       = local.lambdas
  key            = "src/lambdas/${each.value}"
  source         = "${local.src_path}/lambdas/${each.value}"
  source_hash    = filemd5("${local.src_path}/lambdas/${each.value}")
}

# Uploads glue source code to s3
resource "aws_s3_object" "s3_object_glue" {
  bucket = aws_s3_bucket.s3_bucket.id
  key = "src/glue/${local.glue_main}"
  source = "${local.src_path}/glue_job/${local.glue_main}"
  source_hash = filemd5("${local.src_path}/glue_job/${local.glue_main}")
}