provider "aws" {
  region = "us-east-1"
}

module "s3" {
  source      = "./modules/s3"
  bucket_name = "my-data-pipeline"
}

module "glue" {
  source               = "./modules/glue"
  glue_script_location = "s3://${module.s3.bucket_name}/scripts/etl_script.py"
  s3_bucket_name       = module.s3.bucket_name
}

module "mwaa" {
  source            = "./modules/mwaa"
  dags_s3_bucket    = module.s3.bucket_name
  dags_s3_prefix    = "dags/"
  airflow_env_name  = "data-pipeline-airflow"
}
