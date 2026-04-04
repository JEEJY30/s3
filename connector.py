import os
import boto3
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.environ["aws_access_key_id"],
    aws_secret_access_key=os.environ["aws_secret_access_key"],
    aws_session_token=os.environ.get("aws_session_token"),
    region_name=os.environ.get("aws_default_region"),
)


def get_s3_client():
    return session.client("s3")


def get_s3_resource():
    return session.resource("s3")
