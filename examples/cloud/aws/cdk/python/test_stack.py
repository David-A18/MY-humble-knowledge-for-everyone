from aws_cdk import App
from aws_cdk.assertions import Template, Match
from stack import create_stack

template = Template.from_stack(create_stack(App()))
template.resource_count_is("AWS::S3::Bucket", 1)
template.has_resource_properties("AWS::S3::Bucket", {
    "BucketEncryption": {"ServerSideEncryptionConfiguration": [
        {"ServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]},
    "PublicAccessBlockConfiguration": {"BlockPublicAcls": True, "BlockPublicPolicy": True,
        "IgnorePublicAcls": True, "RestrictPublicBuckets": True},
    "VersioningConfiguration": {"Status": "Enabled"},
})
template.has_resource("AWS::S3::Bucket", {"DeletionPolicy": "Retain", "UpdateReplacePolicy": "Retain"})
template.has_resource_properties("AWS::S3::BucketPolicy", {
    "PolicyDocument": {"Statement": Match.array_with([Match.object_like({
        "Effect": "Deny", "Action": "s3:*",
        "Condition": {"Bool": {"aws:SecureTransport": "false"}},
    })])},
})
print("CDK Python security assertions passed")
