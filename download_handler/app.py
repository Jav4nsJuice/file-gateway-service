import boto3
import os
import json
from botocore.config import Config

def lambda_handler(event, context):
    # Log the event to CloudWatch Logs (helpful for debugging 404s/500s)
    print(f"Event Received: {json.dumps(event)}")
    
    bucket_name = os.environ['BUCKET_NAME']
    aws_region = 'us-east-2'

    # Force regional endpoint to ensure URL consistency
    endpoint_url = f"https://s3.{aws_region}.amazonaws.com"
    s3_config = Config(
        region_name=aws_region,
        signature_version='s3v4'
    )

    s3_client = boto3.client(
        's3', 
        endpoint_url=endpoint_url, 
        config=s3_config
    )

    # Robust path parameter retrieval
    # HTTP APIs store these in 'pathParameters'
    path_params = event.get('pathParameters', {})
    object_key = path_params.get('objectKey')

    if not object_key:
        return {
            "statusCode": 400, 
            "body": json.dumps({"error": "objectKey is required in path"})
        }

    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=3600
        )

        return {
            "statusCode": 307,
            "headers": {
                "Location": presigned_url,
                "Access-Control-Allow-Origin": "*" # Helps with browser testing
            }
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
