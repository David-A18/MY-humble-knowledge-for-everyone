from aws_cdk import App, Stack, RemovalPolicy
from aws_cdk import aws_s3 as s3

def create_stack(app: App) -> Stack:
    stack = Stack(app, "KbDocsLab")
    s3.Bucket(stack, "Data", encryption=s3.BucketEncryption.S3_MANAGED,
              block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
              versioned=True, enforce_ssl=True, removal_policy=RemovalPolicy.RETAIN)
    return stack
