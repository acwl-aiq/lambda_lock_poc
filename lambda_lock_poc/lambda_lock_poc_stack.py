from aws_cdk import Stack
from constructs import Construct
from construct.poc_service import PocService


class LambdaLockPocStack(Stack):
    def __init__(self, scope: Construct, stack_id: str, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)
        print(PocService)
        PocService(self, 'PocService')
