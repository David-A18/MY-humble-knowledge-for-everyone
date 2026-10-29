import { App, Stack, RemovalPolicy } from "aws-cdk-lib";
import * as s3 from "aws-cdk-lib/aws-s3";

export function createStack(app: App): Stack {
  const stack = new Stack(app, "KbDocsLab");
  new s3.Bucket(stack, "Data", {
    encryption: s3.BucketEncryption.S3_MANAGED,
    blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
    versioned: true,
    enforceSSL: true,
    removalPolicy: RemovalPolicy.RETAIN,
  });
  return stack;
}
