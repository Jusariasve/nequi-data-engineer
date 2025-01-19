resource "aws_iam_role" "glue_role" {
  name = "glue_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_policy" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_s3_bucket_object" "etl_script" {
  bucket = var.s3_bucket_name
  key    = "scripts/etl_script.py"
  source = "../../../glue_code/etl_script.py" # Ruta local del script
}

resource "aws_glue_job" "etl_job" {
  name        = "etl_job"
  role_arn    = aws_iam_role.glue_role.arn
  command {
    name            = "glueetl"
    script_location = "s3://${var.s3_bucket_name}/scripts/etl_script.py" # Ruta al script
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"      = "python"
    "--extra-py-files"    = "s3://${var.s3_bucket_name}/dependencies/"
    "--RAW_BUCKET"        = "${var.raw_bucket_name}"
    "--PROCESSED_BUCKET"  = "${var.processed_bucket_name}"
    "--ENRICHED_BUCKET"   = "${var.enriched_bucket_name}"
    "--enable-metrics"    = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog" = "true"
  }

  max_capacity      = 2
  timeout           = 10
  glue_version      = "3.0"
  worker_type       = "Standard"
  number_of_workers = 2
}

output "glue_job_name" {
  value = aws_glue_job.etl_job.name
}
