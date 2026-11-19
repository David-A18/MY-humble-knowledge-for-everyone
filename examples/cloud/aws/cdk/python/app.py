from aws_cdk import App
from stack import create_stack
import os
app = App(outdir=os.environ.get("CDK_OUTDIR", "cdk.out"))
create_stack(app)
app.synth()
