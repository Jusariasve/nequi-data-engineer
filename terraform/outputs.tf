output "s3_bucket_name" {
  value = module.s3.bucket_name
}

output "glue_job_name" {
  value = module.glue.glue_job_name
}

output "mwaa_env_name" {
  value = module.mwaa.mwaa_env_name
}
