resource "aws_sfn_state_machine" "stepfunction" {
  name     = "tha-orchestration"
  role_arn = aws_iam_role.sfn_role.arn
  definition = templatefile("${path.module}/resources/pipeline-sfn.tmpl", {
    s3_bucket = aws_s3_bucket.s3_bucket.id
    region = var.region
    account_id = var.account_id
    lambda_func = aws_lambda_function.load_data_to_dynamo.id
    glue_job_name = aws_glue_job.compute_banners.id
  })
}