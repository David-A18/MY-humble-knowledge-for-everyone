import { App } from "aws-cdk-lib";
import { Template, Match } from "aws-cdk-lib/assertions";
import { createStack } from "./stack";
const template = Template.fromStack(createStack(new App()));
template.resourceCountIs("AWS::S3::Bucket", 1);
template.hasResourceProperties("AWS::S3::Bucket", {
  BucketEncryption: { ServerSideEncryptionConfiguration: [
    { ServerSideEncryptionByDefault: { SSEAlgorithm: "AES256" } }] },
  PublicAccessBlockConfiguration: { BlockPublicAcls: true, BlockPublicPolicy: true,
    IgnorePublicAcls: true, RestrictPublicBuckets: true },
  VersioningConfiguration: { Status: "Enabled" },
});
template.hasResource("AWS::S3::Bucket", {
  DeletionPolicy: "Retain", UpdateReplacePolicy: "Retain",
});
template.hasResourceProperties("AWS::S3::BucketPolicy", {
  PolicyDocument: { Statement: Match.arrayWith([Match.objectLike({
    Effect: "Deny", Action: "s3:*",
    Condition: { Bool: { "aws:SecureTransport": "false" } },
  })]) },
});
console.log("CDK TypeScript security assertions passed");
