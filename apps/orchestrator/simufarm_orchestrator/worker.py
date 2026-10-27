"""Runtime/lifecycle work is not started before the v3 stage gates."""
def health():
    return {"status":"disabled-stage-a", "runtime":"redroid-arm64-planned",
            "containers_running":0, "validated_concurrency":None,
            "launch_enabled":False, "lifecycle_stage":"G"}
