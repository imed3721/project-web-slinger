data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "drift_test" {
  bucket = "web-slinger-drift-${data.aws_caller_identity.current.account_id}"

  tags = {
    Project     = "WebSlinger"
    Environment = "Learning"
    DriftTest   = "expected"
  }
}
