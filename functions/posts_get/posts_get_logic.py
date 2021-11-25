import base64

import requests


def posts_get_logic(dynamodb_client, dynamodb_table, s3_client, s3_bucket):
    '''
        Scenario

        !!! IMPORTANT !!!: it is not realistic, but useful to write a test case

        On S3 is stored the content of blog posts
        On DyanomoDB, for each object stored on S3, is stored the information
        about the author (and hypotetically other meta information)

        The response is an array of posts: each post has a property 'author' and
        a property 'content'
    '''

    posts = []

    list_result = s3_client.list_objects_v2(Bucket=s3_bucket)
    if 'Contents' in list_result:
        items = list_result['Contents']

        for item in items:
            key = item['Key']

            object = s3_client.get_object(Bucket=s3_bucket, Key=key)
            post_meta = dynamodb_client.get_item(
                Key={'id': {'S': key}}, TableName=dynamodb_table)

            post_author = post_meta['Item']['author']['S']
            post_content = object['Body'].read().decode('utf-8')

            cover_image = requests.get('https://via.placeholder.com/600')
            post_cover = png_to_base64(cover_image)

            posts.append({
                'author': post_author,
                'content': post_content,
                'cover': post_cover,
                'id': key
            })

    return posts


def png_to_base64(response):
    uri = ('data:' +
           response.headers['Content-Type'] + ';' +
           'base64,' + base64.b64encode(response.content).decode('utf-8'))

    return uri
