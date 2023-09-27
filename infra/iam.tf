resource "aws_iam_role" "glue_job_role" {
  name               = "glue-job-role"
  assume_role_policy = templatefile("${path.module}/resources/policies/glue-role.tmpl", {})
}

resource "aws_iam_policy" "glue_policy" {
  name        = "glue-policy"
  description = "A policy for AWS Glue Job (tha-vibhavari-bellutagi-assignment)"
  policy      = templatefile("${path.module}/resources/policies/glue-policy.tmpl", {
    s3_bucket = aws_s3_bucket.s3_bucket.id
  })
}

resource "aws_iam_role" "sfn_role" {
  name = "sfn-role"
  assume_role_policy = templatefile("${path.module}/resources/policies/sfn-role.tmpl", {})
}


resource "aws_iam_role_policy" "sfn_policy" {
  name = "lambda-policy"
  role = aws_iam_role.sfn_role.id


  policy = templatefile("${path.module}/resources/policies/sfn-policy.tmpl", {})
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-role"

  assume_role_policy = templatefile("${path.module}/resources/policies/lambda-role.tmpl", {})
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = templatefile("${path.module}/resources/policies/lambda-policy.tmpl", {
    s3_bucket = aws_s3_bucket.s3_bucket.id
  })
}


resource "aws_iam_role_policy_attachment" "glue_policy_attachment" {
  role      = aws_iam_role.glue_job_role.name
  policy_arn = aws_iam_policy.glue_policy.arn
}

# creating s3 vpc endpoint
resource "aws_vpc_endpoint" "s3_endpoint" {
  vpc_id       = local.vars.vpc_id
  service_name = "com.amazonaws.${var.region}.s3"
}

# route table
resource "aws_vpc_endpoint_route_table_association" "s3_endpoint_rta" {
  route_table_id  = local.vars.route_table_id
  vpc_endpoint_id = aws_vpc_endpoint.s3_endpoint.id
}


