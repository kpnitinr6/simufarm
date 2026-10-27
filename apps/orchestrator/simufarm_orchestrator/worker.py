"""Free-path orchestration is deliberately disabled until compatibility/approval gates pass."""

MAX_CONCURRENT_EMULATORS = 1


def health():
    return {
        "status": "blocked",
        "max_concurrent_emulators": MAX_CONCURRENT_EMULATORS,
        "emulator_launch_enabled": False,
        "reason": "Oracle account approval and supported ARM/no-KVM runtime are unverified",
    }


if __name__ == "__main__":
    import json

    print(json.dumps(health()))
