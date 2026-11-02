# Stage D capacity actuals — 2 November 2026

**VM installation and two-container boot/APK checks succeeded. Strict four-field identity gate FAILED.**

Target: user-confirmed2TB Seagate external disk, APFS SimuFarmDrive. UTM5.0.8 QEMU/HVF,4vCPU/8192MiB,128GiB sparse virtual disk physically at `/Volumes/SimuFarmDrive/SimuFarm/VMs/SimuFarm.utm/`. Guest Ubuntu22.04, ARM64, kernel5.15.0-202-generic. Guest observed4CPUs and MemTotal8119260kB; KVM absent, binderfs mounted, stock Binder/ashmem modules available. Docker and ADB verified. SSH127.0.0.1:2222 key-authenticated after host-key verification via local UTM guest agent. No unrestricted passwordless sudo or Docker-group membership was granted; administrative diagnostics use the existing guest-agent channel.

| Container | Boot to sys.boot_completed=1 | Docker RAM sampled with both running | Verified sample APK install |
|---|---:|---:|---|
| 1 | 11.435s | 719.6MiB | Success |
| 2 | 13.374s | 757MiB | Success |

Cgroup memory.current measured770760704bytes and808247296bytes respectively. Docker's displayed memory excludes some cache and is not identical to raw cgroup accounting. These are one-run observations, not a capacity/concurrency guarantee. Boot timing starts immediately before docker run and ends at Android boot completion; RAM was sampled after the second container booted.

| Identity field | Observed result |
|---|---|
| android_id | Present and different |
| adb_serial | 127.0.0.1:5555 vs127.0.0.1:5556, different |
| IMEI | null for both — FAIL |
| ro.serialno | empty for both — FAIL |

No replacement or spoofed identities were generated. No complete runtime profile was promoted. StageE remains unstarted. A separate reviewed identity policy/implementation is needed to satisfy the strict StageD gate; do not label this fully green.

Pinned Redroid13ARM64 image: `redroid/redroid@sha256:c815ac1b1d5bd0a099b74c3e3e0eeea3b32bed8d7ab1f788c20fb74e35891716`. Official Appium6.0.18 debug APK SHA256:a9eecf37b26cd084855c530db81c2bb1b91f4c1b095a04f47aa7c20e2791f686. Both installs returned Success and both ADB states were device. Both published ADB ports bind only to guest127.0.0.1.

Final inventory:2running validated-run containers plus1stopped first-run container retained for inspection. Three containers were created across the two test attempts; do not misreport that history as only2ever created. The first official release APK passed its digest but Android rejected its certificate; first-run evidence is preserved. Installer failures and their preserved disk are documented in STAGE_D_UTM.md.

Raw identities/evidence are local and excluded from public Git: `data/runtime/local/utm-20261102/observations.json`, mirrored on external drive under `SimuFarm/evidence/runtime/36ccc1fa8afa40a4bb9f70b6afe03bc9/evidence/observations.json`. No Oracle or MobileAPI calls for the UTM setup, and no billable cloud resources provisioned. Historical Oracle network cleanup remains a separate user-run action; it has not been performed or verified here.
