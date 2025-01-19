variable "raw_bucket_name" {
  description = "Nombre del bucket para la capa raw"
  type        = string
}

variable "processed_bucket_name" {
  description = "Nombre del bucket para la capa processed"
  type        = string
}

variable "enriched_bucket_name" {
  description = "Nombre del bucket para la capa enriched"
  type        = string
}

variable "s3_bucket_name" {
  description = "Nombre del bucket S3 donde se almacenarán scripts y dependencias"
  type        = string
}