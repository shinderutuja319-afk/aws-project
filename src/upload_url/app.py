import json
import os
import uuid
import boto3

from botocore.config import Config

s3 = boto3.client(
    "s3",
    region_name="ap-south-1",
    endpoint_url="https://s3.ap-south-1.amazonaws.com",
    config=Config(signature_version="s3v4"),
)

BUCKET_NAME = os.environ["BUCKET_NAME"]


def lambda_handler(event, context):

    resume_id = str(uuid.uuid4())

    object_key = f"resumes/{resume_id}.pdf"

    upload_url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": object_key,
            "ContentType": "application/pdf"
        },
        ExpiresIn=300
    )

    response = {
        "resume_id": resume_id,
        "upload_url": upload_url,
        "object_key": object_key,
        "expires_in": 300
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }