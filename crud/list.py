from connector import get_s3_client


def list_buckets():
    s3 = get_s3_client()
    response = s3.list_buckets()
    for bucket in response["Buckets"]:
        print(bucket["Name"])


def list_objects(bucket, prefix=""):
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if "Contents" not in response:
        print("No objects found.")
        return
    for obj in response["Contents"]:
        print(f'{obj["Key"]}  ({obj["Size"]} bytes)')
