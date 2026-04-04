import os
import magic
from connector import get_s3_client


def upload_file(file_path, bucket, key=None):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if key is None:
        key = os.path.basename(file_path)

    content_type = magic.from_file(file_path, mime=True)

    s3 = get_s3_client()
    s3.upload_file(
        file_path,
        bucket,
        key,
        ExtraArgs={"ContentType": content_type},
    )

    print(f"Uploaded {file_path} -> s3://{bucket}/{key} ({content_type})")
