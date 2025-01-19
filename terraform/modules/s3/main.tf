resource "aws_s3_bucket" "bucket" {
  bucket        = var.bucket_name
  acl           = "private"
  force_destroy = true
}

resource "aws_s3_bucket_object" "folders" {
  for_each = toset(["raw/", "processed/", "enriched/", "scripts/", "dags/"])
  bucket   = aws_s3_bucket.bucket.id
  key      = each.value
}

output "bucket_name" {
  value = aws_s3_bucket.bucket.id
}
