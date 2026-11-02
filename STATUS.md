# SimuFarm status — 2 November 2026

External-drive UTM Ubuntu22.04 ARM64 setup is operational:4CPUs/8GB, localhostSSH2222, Docker, Binder/ashmem and binderfs verified. Two Redroid13containers booted and each installed the verified signed sample APK. Boot times11.435s/13.374s; Docker RAM719.6MiB/757MiB with both running.

**StageD strict identity gate remains FAILED**: android_id and adb_serial differ, but both IMEIs are null and both hardware serials are empty. No values were invented. StageE remains unstarted and human-reviewed runtime-eligible subset remains0. See docs/CAPACITY.md for actuals and docs/STAGE_D_UTM.md for setup/recovery details.

Oracle launch scripts remain disabled and ADR015 superseded. No Oracle/MobileAPI calls or billable cloud provisioning occurred for the UTM setup. Ordinary SSH retains standard permissions; privileged diagnostics use the existing UTM guest agent, with no unrestricted passwordless sudo grant.

C2 engineering and seven C2.1 unknown-geometry deviations were previously accepted. Generated-artifact integration from the cloud-conflicted original checkout remains separate; no new static-data verification claim is made by this VM work.
