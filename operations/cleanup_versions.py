from datetime import datetime, timezone, timedelta
from connector import get_s3_client


def cleanup_old_versions(bucket, prefix="", months=6, dry_run=True):
    s3 = get_s3_client()
    cutoff = datetime.now(timezone.utc) - timedelta(days=months * 30)

    paginator = s3.get_paginator("list_object_versions")
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

    to_delete = []

    for page in pages:
        for version in page.get("Versions", []):
            if version["IsLatest"]:
                continue
            if version["LastModified"] < cutoff:
                to_delete.append({
                    "Key": version["Key"],
                    "VersionId": version["VersionId"],
                    "LastModified": version["LastModified"],
                })

        for marker in page.get("DeleteMarkers", []):
            if marker["IsLatest"]:
                continue
            if marker["LastModified"] < cutoff:
                to_delete.append({
                    "Key": marker["Key"],
                    "VersionId": marker["VersionId"],
                    "LastModified": marker["LastModified"],
                })

    if not to_delete:
        print("No versions older than 6 months found.")
        return

    print(f"Found {len(to_delete)} old version(s) before {cutoff.date()}:\n")
    for item in to_delete:
        print(f"  {item['Key']}  v={item['VersionId'][:8]}...  ({item['LastModified'].date()})")

    if dry_run:
        print(f"\nDry run — no deletions. Use --apply to delete.")
        return

    # Delete in batches of 1000 (S3 limit)
    for i in range(0, len(to_delete), 1000):
        batch = to_delete[i:i + 1000]
        s3.delete_objects(
            Bucket=bucket,
            Delete={
                "Objects": [{"Key": d["Key"], "VersionId": d["VersionId"]} for d in batch],
                "Quiet": True,
            },
        )

    print(f"\nDeleted {len(to_delete)} old version(s).")
