from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_apigateway,
    aws_events,
    aws_events_targets,
    RemovalPolicy,
    Duration
)
from constructs import Construct


class PocService(Construct):

    def __init__(self, scope, id):
        super().__init__(scope, id)

        ddb_lock_table = ddb.Table(
            self, "PocLockTable",
            table_name="poc_lock_table2",
            partition_key={
                "name": "token_key",
                "type": ddb.AttributeType.STRING
            },
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY  # NOT recommended for production code
        )

        api_gw_handler = _lambda.Function(self, "requestHandler",
            handler="activity.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.AssetCode("lib"),
            timeout=Duration.minutes(11),
            environment={
                "LOCK_TABLE_NAME": ddb_lock_table.table_name,
                "SLEEP_SECONDS": "5"
            }
        )


        api = aws_apigateway.RestApi(self, "PocApiGateway",
            rest_api_name="PocAPI",
            description="Test idempotency lock with DDB."
        )


        get_handler = aws_apigateway.LambdaIntegration(api_gw_handler,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        api.root.add_method("GET", get_handler)

        canary_handler = _lambda.Function(self, "canaryHandler",
            handler="canary.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.AssetCode("lib"),
            timeout=Duration.seconds(60),
            environment={
                "API_GW_URL": api.url,
                "PROBED_IDEMPOTENCY_TOKEN": "123"
            }
        )

        canary_event_target = aws_events_targets.LambdaFunction(canary_handler)

        aws_events.Rule(self, 'CanaryScheduleRule',
            schedule=aws_events.Schedule.rate(Duration.minutes(1)),
            targets=[canary_event_target]
        )

        ddb_lock_table.grant_read_write_data(api_gw_handler.role)
