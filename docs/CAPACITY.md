# Runtime capacity actuals

As of 2026-10-28, Stage D is authorized but **not executed**. Oracle credentials, account-specific unused free allowance evidence, deployment parameters and a reachable ARM host are unavailable to this task.

| Observation | Actual |
| --- | --- |
| Oracle VMs provisioned | 0 |
| Containers booted | 0 |
| ADB connections verified | 0 |
| APK installations verified | 0 |
| `/dev/kvm` absence | Not observed |
| binder/ashmem modules | Not observed |
| Container 1 boot seconds / RAM | Not measured |
| Container 2 boot seconds / RAM | Not measured |
| Four identity fields distinct | Not tested |
| MobileAPI calls | 0 |
| Billable resources touched | 0 |

The 2 OCPU / 12 GB VM is a target, not an actual allocation or a capacity benchmark. No concurrency claim is made. Raw runtime evidence will be recorded under `data/runtime/<run>/observations.json` using `scripts/stage_d_remote.py`; failures and missing values must remain visible. See [readiness procedure](STAGE_D_READINESS.md).

Stage E is blocked until C2 is complete and >=1 complete human-reviewed runtime profile exists; X100 India/China identity consistency is a separate mandatory preflight.
