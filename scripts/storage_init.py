"""Idempotent local S3 bucket init. Never provisions paid cloud resources."""

import os
import time

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError


def ensure_bucket(client, bucket):
    try:
        client.head_bucket(Bucket=bucket)
    except ClientError as exc:
        code = str(exc.response.get("Error", {}).get("Code", ""))
        if code not in {"404", "NoSuchBucket", "NotFound"}:
            raise
        try:
            client.create_bucket(Bucket=bucket)
        except ClientError as create_exc:
            # An initializer race is safe only if this account owns the bucket.
            if create_exc.response.get("Error", {}).get("Code") != "BucketAlreadyOwnedByYou":
                raise
        client.head_bucket(Bucket=bucket)


def main():
    endpoint = os.environ["S3_ENDPOINT"]
    # This bootstrap job is local-only; cloud endpoint init needs separate approval.
    if endpoint not in {"http://minio:9000", "http://127.0.0.1:9000", "http://localhost:9000"}:
        raise ValueError("Bootstrap initializer accepts local MinIO endpoints only")
    client = boto3.client("s3", endpoint_url=endpoint, region_name="us-east-1")
    deadline = time.monotonic() + 90
    while True:
        try:
            ensure_bucket(client, os.environ["S3_BUCKET"])
            print("MinIO bucket initialized and accessible")
            return
        except EndpointConnectionError:
            if time.monotonic() >= deadline:
                raise
            time.sleep(2)


if __name__ == "__main__":
    main()
