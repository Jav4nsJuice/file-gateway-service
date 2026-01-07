import json
import boto3
import os
from botocore.config import Config

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    aws_region = 'us-east-2'
    
    # 1. Force the client to use the regional endpoint URL directly
    endpoint_url = f"https://s3.{aws_region}.amazonaws.com"
    
    s3_config = Config(
        region_name=aws_region,
        signature_version='s3v4'
    )
    
    # 2. Initialize with the explicit endpoint_url
    s3_client = boto3.client(
        's3', 
        endpoint_url=endpoint_url, 
        config=s3_config
    )
    
    try:
        body = json.loads(event.get('body', '{}'))
        file_name = body.get('filename', 'test-file.txt')

        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': file_name},
            ExpiresIn=3600
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "uploadUrl": presigned_url, 
                "objectKey": file_name
            })
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
