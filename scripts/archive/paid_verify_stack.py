"""Run inside the API container after Compose starts; exits nonzero on any failure."""

import json
import os
import uuid
from urllib.request import urlopen

import boto3
import psycopg
from redis import Redis


def main():
    with urlopen("http://127.0.0.1:8000/health/live", timeout=10) as response:
        assert json.load(response)["status"] == "ok"
    with psycopg.connect(os.environ["DATABASE_URL"], connect_timeout=10) as conn:
        assert conn.execute("SELECT 1").fetchone() == (1,)
        assert conn.execute("SELECT to_regclass('public.device_profiles')").fetchone()[0]
    redis = Redis.from_url(os.environ["REDIS_URL"], socket_connect_timeout=10)
    assert redis.ping()
    client = boto3.client("s3", endpoint_url=os.environ["S3_ENDPOINT"], region_name="us-east-1")
    bucket = os.environ["S3_BUCKET"]
    client.head_bucket(Bucket=bucket)
    key = f"bootstrap-smoke/{uuid.uuid4()}.txt"
    body = b"simufarm-storage-roundtrip"
    try:
        client.put_object(Bucket=bucket, Key=key, Body=body)
        response = client.get_object(Bucket=bucket, Key=key)
        with response["Body"] as stream:
            assert stream.read() == body
    finally:
        client.delete_object(Bucket=bucket, Key=key)
    print(
        json.dumps(
            {
                "api": "passed",
                "postgres": "passed",
                "redis": "passed",
                "minio_bucket": "passed",
                "object_roundtrip": "passed",
            }
        )
    )


if __name__ == "__main__":
    main()
