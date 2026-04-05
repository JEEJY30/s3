from connector import get_s3_client


def check_versioning(bucket):
    s3 = get_s3_client()
    response = s3.get_bucket_versioning(Bucket=bucket)
    status = response.get("Status", "Disabled")
    print(f"Bucket: {bucket}")
    print(f"Versioning: {status}")


def file_versions(bucket, key):
    s3 = get_s3_client()
    response = s3.list_object_versions(Bucket=bucket, Prefix=key)

    versions = [v for v in response.get("Versions", []) if v["Key"] == key]

    if not versions:
        print(f"No versions found for {key}")
        return

    print(f"File: {key}")
    print(f"Total versions: {len(versions)}\n")
    for v in versions:
        latest = " (latest)" if v["IsLatest"] else ""
        print(f"  {v['VersionId'][:12]}...  {v['LastModified'].strftime('%Y-%m-%d %H:%M:%S')}{latest}")


def restore_previous_version(bucket, key):
    s3 = get_s3_client()
    response = s3.list_object_versions(Bucket=bucket, Prefix=key)

    versions = [v for v in response.get("Versions", []) if v["Key"] == key]

    if len(versions) < 2:
        print(f"No previous version to restore for {key}")
        return

    previous = versions[1]
    prev_id = previous["VersionId"]

    s3.copy_object(
        Bucket=bucket,
        Key=key,
        CopySource={"Bucket": bucket, "Key": key, "VersionId": prev_id},
    )

    print(f"Restored {key} from version {prev_id[:12]}... ({previous['LastModified'].strftime('%Y-%m-%d %H:%M:%S')})")
