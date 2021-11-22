import io
import os
import unittest

import boto3
from botocore.response import StreamingBody
from botocore.stub import Stubber

from functions.posts_get.posts_get_logic import posts_get_logic


class GetSomethingLogicTest(unittest.TestCase):
    def setUp(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp
        os.environ['AWS_DEFAULT_REGION'] = 'eu-west-1'

    def tearDown(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.tearDown
        pass

    def __creeate_s3_object_body(self, content: str):
        return StreamingBody(
            io.BytesIO(content.encode()),
            len(content)
        )

    def test_get_something(self):
        DYNAMODB_TABLE = 'test-posts-meta'
        S3_BUCKET = 'test-posts'
        POST_1_KEY = 'post_2021-11-15T10:00:00Z.html'
        POST_2_KEY = 'post_2021-11-16T10:00:00Z.html'

        # region ------------------------------------------------- DynamoDB Stub
        dynamodb_client = boto3.client('dynamodb')
        dynamodb_stubber = Stubber(dynamodb_client)
        # region ------------------------------------------------------ 1st call
        dynamodb_stubber.add_response(
            'get_item',
            {
                'Item': {
                    'author': {'S': 'Elia Contini'},
                    'id': {'S': POST_1_KEY}
                }
            },
            {
                'Key': {'id': {'S': POST_1_KEY}},
                'TableName': DYNAMODB_TABLE
            }
        )
        # endregion ------------------------------------------------------------

        # region ------------------------------------------------------ 2nd call
        dynamodb_stubber.add_response(
            'get_item',
            {
                'Item': {
                    'author': {'S': 'Piero Bozzolo'},
                    'id': {'S': POST_2_KEY}
                }
            },
            {
                'Key': {'id': {'S': POST_2_KEY}},
                'TableName': DYNAMODB_TABLE
            }
        )
        # endregion ------------------------------------------------------------

        dynamodb_stubber.activate()
        # endregion ------------------------------------------------------------

        # region ------------------------------------------------------- S3 Stub
        s3_client = boto3.client('s3')
        s3_stubber = Stubber(s3_client)
        # region ------------------------------------------------------ 1st call
        list_objects_v2_expected_params = {'Bucket': S3_BUCKET}
        list_objects_v2_expected_result = {
            'Contents': [{'Key': POST_1_KEY}, {'Key': POST_2_KEY}]
        }
        s3_stubber.add_response(
            'list_objects_v2',
            list_objects_v2_expected_result,
            list_objects_v2_expected_params
        )
        # endregion ------------------------------------------------------------

        # region ------------------------------------------------------ 2nd call
        get_object_expected_params = {'Bucket': S3_BUCKET, 'Key': POST_1_KEY}
        get_object_expected_result = {
            'Body': self.__creeate_s3_object_body(
                '<h1>Post 1</h1><p>Content 1.</p>'
            )
        }
        s3_stubber.add_response(
            'get_object',
            get_object_expected_result,
            get_object_expected_params
        )
        # endregion ------------------------------------------------------------

        # region ------------------------------------------------------ 3rd call
        get_object_expected_params = {'Bucket': S3_BUCKET, 'Key': POST_2_KEY}
        get_object_expected_result = {
            'Body': self.__creeate_s3_object_body(
                '<h1>Post 2</h1><p>Content 2.</p>'
            )
        }
        s3_stubber.add_response(
            'get_object',
            get_object_expected_result,
            get_object_expected_params
        )
        # endregion ------------------------------------------------------------

        s3_stubber.activate()
        # endregion ------------------------------------------------------------

        result = posts_get_logic(
            dynamodb_client, DYNAMODB_TABLE, s3_client, S3_BUCKET)

        self.assertEqual(len(result), 2)

        dynamodb_stubber.assert_no_pending_responses()
        s3_stubber.assert_no_pending_responses()
