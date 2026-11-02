# Runtime capacity actuals — 31 October 2026

Stage D now targets a user-owned Ubuntu22.04 server over Meshnet. **Prepared; awaiting IP and SSH username.** No server connection or runtime benchmark has occurred. Oracle retry process stopped after16attempts on29October (HTTP429); it is absent and disabled. No Oracle VM was returned. Free Oracle network prerequisites remain pending user-run cleanup; no Oracle API calls were made for this pivot.

| Observation | Actual |
| --- | --- |
| Oracle VMs provisioned | 0 |
| Containers booted | 0 |
| ADB connections verified | 0 |
| APK installations verified | 0 |
| `/dev/kvm` presence (optional) | Not observed |
| binder/ashmem modules | Not observed |
| Container 1 boot seconds / RAM | Not measured |
| Container 2 boot seconds / RAM | Not measured |
| Four identity fields distinct | Not tested |
| MobileAPI calls | 0 |
| Billable resources touched | 0 |

Hardware architecture, CPU count, RAM and disk are unknown until SSH preflight. No concurrency/capacity figure is promised. KVM presence is recorded, not a requirement. The server's binder/ashmem availability and an architecture-matching immutable Redroid image must be verified before booting containers. Evidence will be fetched under `data/runtime/local/<run>/`. No identity values or measurements are invented. See [local deployment procedure](STAGE_D_LOCAL.md).

StageE remains unstarted; at least1 complete human-reviewed runtime-eligible profile and the X100 region decision are still required. StageD diagnostics do not promote profiles.
