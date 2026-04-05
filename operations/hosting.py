import os
import json
import subprocess
import magic
from connector import get_s3_client


def enable_static_hosting(bucket, index="index.html", error="index.html"):
    s3 = get_s3_client()

    # disable block public access
    s3.put_public_access_block(
        Bucket=bucket,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False,
        },
    )

    # set public read bucket policy
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket}/*",
            }
        ],
    }
    s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))

    # enable static website hosting
    s3.put_bucket_website(
        Bucket=bucket,
        WebsiteConfiguration={
            "IndexDocument": {"Suffix": index},
            "ErrorDocument": {"Key": error},
        },
    )

    region = s3.get_bucket_location(Bucket=bucket).get("LocationConstraint") or "us-east-1"
    if region == "us-east-1":
        url = f"http://{bucket}.s3-website-us-east-1.amazonaws.com"
    else:
        url = f"http://{bucket}.s3-website-{region}.amazonaws.com"

    print(f"Static hosting enabled on: {bucket}")
    print(f"URL: {url}")
    return url


def upload_directory(bucket, directory):
    s3 = get_s3_client()
    count = 0

    for root, _, files in os.walk(directory):
        for filename in files:
            local_path = os.path.join(root, filename)
            key = os.path.relpath(local_path, directory)
            content_type = magic.from_file(local_path, mime=True)

            s3.upload_file(
                local_path,
                bucket,
                key,
                ExtraArgs={"ContentType": content_type},
            )
            count += 1
            print(f"  {key} ({content_type})")

    print(f"\nUploaded {count} file(s) to s3://{bucket}/")


def deploy_react(bucket, project_dir):
    build_dir = os.path.join(project_dir, "build")

    print(f"Building React project in {project_dir}...")
    subprocess.run(["npm", "install"], cwd=project_dir, check=True)
    subprocess.run(["npm", "run", "build"], cwd=project_dir, check=True)

    if not os.path.isdir(build_dir):
        raise FileNotFoundError(f"Build directory not found: {build_dir}")

    print(f"\nUploading build to s3://{bucket}/...")
    upload_directory(bucket, build_dir)

    url = enable_static_hosting(bucket)
    print(f"\nReact app deployed: {url}")
