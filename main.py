import argparse
from crud.upload import upload_file
from crud.list import list_buckets, list_objects
from operations.cleanup_versions import cleanup_old_versions
from operations.versioning import check_versioning, file_versions, restore_previous_version
from operations.hosting import enable_static_hosting, upload_directory, deploy_react


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

    # cleanup-versions
    cleanup_parser = subparsers.add_parser("cleanup-versions", help="Delete object versions older than 6 months")
    cleanup_parser.add_argument("bucket", help="Target S3 bucket name")
    cleanup_parser.add_argument("--prefix", default="", help="Filter by key prefix")
    cleanup_parser.add_argument("--months", type=int, default=6, help="Age threshold in months (default: 6)")
    cleanup_parser.add_argument("--apply", action="store_true", help="Actually delete (default is dry run)")

    # versioning
    ver_parser = subparsers.add_parser("versioning", help="Check if versioning is enabled")
    ver_parser.add_argument("bucket", help="Target S3 bucket name")

    # file-versions
    fv_parser = subparsers.add_parser("file-versions", help="Show version count and dates for a file")
    fv_parser.add_argument("bucket", help="Target S3 bucket name")
    fv_parser.add_argument("file", help="S3 object key")

    # restore
    restore_parser = subparsers.add_parser("restore", help="Restore previous version as latest")
    restore_parser.add_argument("bucket", help="Target S3 bucket name")
    restore_parser.add_argument("file", help="S3 object key")

    # host-static
    host_parser = subparsers.add_parser("host-static", help="Enable static website hosting and upload files")
    host_parser.add_argument("bucket", help="Target S3 bucket name")
    host_parser.add_argument("directory", help="Local directory to upload")
    host_parser.add_argument("--index", default="index.html", help="Index document (default: index.html)")
    host_parser.add_argument("--error", default="index.html", help="Error document (default: index.html)")

    # deploy-react
    react_parser = subparsers.add_parser("deploy-react", help="Build and deploy a React app to S3")
    react_parser.add_argument("bucket", help="Target S3 bucket name")
    react_parser.add_argument("project", help="Path to React project directory")

    args = parser.parse_args()

    if args.command == "upload":
        upload_file(args.file, args.bucket, args.key)
    elif args.command == "list":
        if args.bucket:
            list_objects(args.bucket, args.prefix)
        else:
            list_buckets()
    elif args.command == "cleanup-versions":
        cleanup_old_versions(args.bucket, args.prefix, args.months, dry_run=not args.apply)
    elif args.command == "versioning":
        check_versioning(args.bucket)
    elif args.command == "file-versions":
        file_versions(args.bucket, args.file)
    elif args.command == "restore":
        restore_previous_version(args.bucket, args.file)
    elif args.command == "host-static":
        upload_directory(args.bucket, args.directory)
        enable_static_hosting(args.bucket, args.index, args.error)
    elif args.command == "deploy-react":
        deploy_react(args.bucket, args.project)


if __name__ == "__main__":
    main()
