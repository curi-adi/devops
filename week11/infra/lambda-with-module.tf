module "lambda_function" {
  for_each = local.lambda_functions

  source  = "terraform-aws-modules/lambda/aws"
  version = "8.7.0"

  function_name = each.value.function_name
  description   = each.value.description
  handler       = each.value.handler
  runtime       = "python3.14"
  publish       = true

  create_role = false
  lambda_role = aws_iam_role.lambda_role[each.key].arn

  source_path = each.value.source_dir

  store_on_s3 = true
  s3_bucket   = "clean-bucket-YOUR_ACCOUNT_ID"

  # layers = [
  #   module.lambda_layer_s3.lambda_layer_arn,
  # ]

  environment_variables = {
    Serverless = "Terraform"
  }

  tags = {
    Module = "lambda-with-layer"
  }
}
