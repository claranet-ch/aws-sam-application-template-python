import json
import logging
import os
import traceback

import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

from posts_get_logic import posts_get_logic

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')


def posts_get(event, context):
    """
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    try:
        dynamodb_table = os.environ.get('TABLE_POSTS')
        s3_bucket = os.environ.get('BUCKET_POSTS')

        result = posts_get_logic(
            dynamodb_client, dynamodb_table, s3_client, s3_bucket)

        return {
            'body': json.dumps(result),
            'statusCode': 200,
        }
    except Exception:
        exception_message = traceback.format_exc()

        logger.exception(exception_message)

        return {
            'body': json.dumps({
                'exception': exception_message,
                'message': 'A short but meaningful message about the issue'
            }),
            'statusCode': 500,
        }
