#!/usr/bin/env python3
from lambda_lock_poc.lambda_lock_poc_stack import LambdaLockPocStack
from aws_cdk import App, Environment


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    stack_env = Environment(account="612099723271", region="us-east-1")
    app = App()
    poc_stack = LambdaLockPocStack(app, 'PocStack', env=stack_env)
    app.synth()
