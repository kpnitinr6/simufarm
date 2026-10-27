import importlib.util
from pathlib import Path
from unittest.mock import Mock

import pytest
from botocore.exceptions import ClientError

spec = importlib.util.spec_from_file_location(
    "storage_init", Path(__file__).resolve().parents[1] / "scripts/storage_init.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def error(code):
    return ClientError({"Error": {"Code": code}}, "HeadBucket")


def test_existing_bucket_is_not_recreated():
    client = Mock()
    module.ensure_bucket(client, "simufarm")
    client.create_bucket.assert_not_called()


def test_missing_bucket_created_and_verified():
    client = Mock()
    client.head_bucket.side_effect = [error("404"), None]
    module.ensure_bucket(client, "simufarm")
    client.create_bucket.assert_called_once_with(Bucket="simufarm")
    assert client.head_bucket.call_count == 2


def test_access_denied_does_not_create_bucket():
    client = Mock()
    client.head_bucket.side_effect = error("403")
    with pytest.raises(ClientError):
        module.ensure_bucket(client, "simufarm")
    client.create_bucket.assert_not_called()


def test_owned_bucket_race_is_safe():
    client = Mock()
    client.head_bucket.side_effect = [error("404"), None]
    client.create_bucket.side_effect = error("BucketAlreadyOwnedByYou")
    module.ensure_bucket(client, "simufarm")


def test_foreign_bucket_conflict_is_not_ignored():
    client = Mock()
    client.head_bucket.side_effect = error("404")
    client.create_bucket.side_effect = error("BucketAlreadyExists")
    with pytest.raises(ClientError):
        module.ensure_bucket(client, "simufarm")
