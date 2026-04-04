import argparse
from crud.upload import upload_file
from crud.list import list_buckets, list_objects


def main():
    parser = argparse.ArgumentParser(
        description="S3 CLI — manage files in AWS S3"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # upload
    upload_parser = subparsers.add_parser("upload", help="Upload a file to S3")
    upload_parser.add_argument("file", help="Path to the local file")
    upload_parser.add_argument("bucket", help="Target S3 bucket name")
    upload_parser.add_argument(
        "--key", default=None, help="S3 object key (defaults to filename)"
    )

    # list
    list_parser = subparsers.add_parser("list", help="List buckets or objects")
    list_parser.add_argument("bucket", nargs="?", default=None, help="Bucket name (omit to list all buckets)")
    list_parser.add_argument("--prefix", default="", help="Filter objects by prefix")

    args = parser.parse_args()

    if args.command == "upload":
        upload_file(args.file, args.bucket, args.key)
    elif args.command == "list":
        if args.bucket:
            list_objects(args.bucket, args.prefix)
        else:
            list_buckets()


if __name__ == "__main__":
    main()
