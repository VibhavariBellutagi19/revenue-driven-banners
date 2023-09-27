resource "aws_lambda_function" "load_data_to_dynamo" {
  function_name = "load_data_to_dynamo"
  handler       = "handler.lambda_handler"
  runtime       = local.vars.python_runtime
  role          = aws_iam_role.lambda_role.arn

  s3_bucket = aws_s3_bucket.s3_bucket.id
  s3_key    = "code/lambdas/${local.vars.push_to_dynamodb}_${local.version}.zip"
  vpc_config {
    security_group_ids = [local.vars.security_group]
    subnet_ids         = [local.vars.subnet_id]
  }
}

/*
resource "aws_lambda_function" "serves_api_requests" {
  function_name = "serve_api"
  handler       = "serve_requests.lambda_handler"
  runtime       = local.vars.python_runtime
  role          = aws_iam_role.lambda_role.arn

  s3_bucket = aws_s3_bucket.s3_bucket.id
  s3_key    = "code/lambdas/${local.vars.serve_requests}"
  vpc_config = {
    security_group_ids = local.vars.security_group
    subnet_ids         = local.vars.subnet_id
  }
}*/
