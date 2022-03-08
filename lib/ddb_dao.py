import boto3
from botocore.exceptions import ClientError


def acquire_lock(table_name, idempotency_token):
    try:
        dynamodb = boto3.client("dynamodb")
        dynamodb.put_item(
            TableName=table_name, Item={"token_key": {"S": idempotency_token}},
            ConditionExpression="attribute_not_exists(token_key)"
        )
        return True
    except ClientError as e:
        return False


def release_lock(table_name, idempotency_token):
    try:
        dynamodb = boto3.client("dynamodb")
        dynamodb.delete_item(
            TableName=table_name, Key={"token_key": {
                'S': idempotency_token}
            }
        )
        return True
    except ClientError as e:
        print(e)
        return False
