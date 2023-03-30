import os
import json
import boto3
import requests
import botocore.exceptions

s3_client = boto3.client("s3")
S3_BUCKET = os.getenv('BUCKET_NAME')

# 1.) Function to get a file from url
# Function to get a file from url


def get_file_from_url(url):
    try:
        response = requests.get(url)
        return response.content
    except botocore.exceptions.ClientError as e:
        print(e)
        return None
    finally:
        pass


# 2.) Function to upload image to S3
def upload_to_s3(file_name, file_content):
    try:
        s3_client.put_object(file_name, file_content, S3_BUCKET)
        return True
    except botocore.exceptions.ClientError as e:
        print(e)
        return False
    finally:
        pass


def handler(event, context):
    url = event["queryStringParameters"]["url"]
    name = event["queryStringParameters"]["name"]

    # pass the output of method #1 as input to method #2
    file_content = get_file_from_url(url)
    upload_to_s3(name, file_content)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully Uploaded Img!')
    }
