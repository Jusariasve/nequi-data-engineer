resource "aws_iam_role" "mwaa_role" {
  name = "mwaa_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "airflow.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "mwaa_policy" {
  role       = aws_iam_role.mwaa_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonMWAAServiceRolePolicy"
}

resource "aws_mwaa_environment" "mwaa_env" {
  name               = var.airflow_env_name
  execution_role_arn = aws_iam_role.mwaa_role.arn
  dag_s3_path        = "${var.dags_s3_prefix}"
  source_bucket_arn  = "arn:aws:s3:::${var.dags_s3_bucket}"

  logging_configuration {
    dag_processing_logs {
      log_level = "INFO"
      enabled   = true
    }
  }
}

output "mwaa_env_name" {
  value = aws_mwaa_environment.mwaa_env.name
}
