output "drift_test_bucket_name" {
  description = "S3 bucket name used for infrastructure drift detection exercises"
  value       = aws_s3_bucket.drift_test.bucket
}

