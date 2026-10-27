"""Stage D identity evidence contract; does not create identifiers or run a device."""


def validate_distinct_identities(first: dict, second: dict) -> None:
    for key in ("container_id", "adb_serial", "android_id", "imei", "device_serial"):
        values = [record.get(key) for record in (first, second)]
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError(f"Missing identity evidence: {key}; do not invent it")
        if values[0] == values[1]:
            raise ValueError(f"Duplicate identity: {key}")
