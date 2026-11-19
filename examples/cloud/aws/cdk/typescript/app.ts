import { App } from "aws-cdk-lib";
import { createStack } from "./stack";
const app = new App({ outdir: process.env.CDK_OUTDIR ?? "cdk.out" });
createStack(app);
app.synth();
