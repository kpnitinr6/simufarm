# Stage D capacity actuals — 2 November 2026

**Stage D ACCEPTED by the user on2November2026.** Missing default IMEI/serial are deferred to authorized StageE identity injection; the frozen diagnostic report is not rewritten.

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
| IMEI | null for both — deferred to Stage E by user |
| ro.serialno | empty for both — deferred to Stage E by user |

These are the original Stage D observations. The user accepted Stage D and authorized Stage E on 2 November 2026; the original strict diagnostic output is retained without rewriting it. No runtime profile was promoted by Stage D.

Pinned Redroid13ARM64 image: `redroid/redroid@sha256:c815ac1b1d5bd0a099b74c3e3e0eeea3b32bed8d7ab1f788c20fb74e35891716`. Official Appium6.0.18 debug APK SHA256:a9eecf37b26cd084855c530db81c2bb1b91f4c1b095a04f47aa7c20e2791f686. Both installs returned Success and both ADB states were device. Both published ADB ports bind only to guest127.0.0.1.

Final inventory:2running validated-run containers plus1stopped first-run container retained for inspection. Three containers were created across the two test attempts; do not misreport that history as only2ever created. The first official release APK passed its digest but Android rejected its certificate; first-run evidence is preserved. Installer failures and their preserved disk are documented in STAGE_D_UTM.md.

Raw identities/evidence are local and excluded from public Git: `data/runtime/local/utm-20261102/observations.json`, mirrored on external drive under `SimuFarm/evidence/runtime/36ccc1fa8afa40a4bb9f70b6afe03bc9/evidence/observations.json`. No Oracle or MobileAPI calls for the UTM setup, and no billable cloud resources provisioned. Historical Oracle network cleanup remains a separate user-run action; it has not been performed or verified here.

## Accepted planning ceiling

Configured ceiling: **5 concurrent containers**, reserving **2GiB for the Ubuntu guest OS** within the8GiB VM. Rounded reference numbers requested by the user: **~11s boot / ~720MiB RAM** (first container11.435s /719.6MiB; second13.374s /757MiB). These remain two-container observations. Five-container concurrency is a planning limit, not a measured capacity result; no5–6container load benchmark has been run. The Mac's own memory budget is separate.

StageE is now explicitly authorized for identity-injection tests. IMEI properties and serials will be synthetic per-instance test identifiers, never represented as original physical handset identifiers. A getprop IMEI value and a telephony-service IMEI result must be reported separately.


## Stage E property test actuals

Two China X100 test containers booted on the derived resetprop image on 2 November 2026. First boots: **9.183s / 12.761s**; restarts: **9.133s / 10.287s**. Docker RAM samples were **636.5MiB / 645.4MiB** after first boots and **667MiB / 681.9MiB** after restarts, under a1200MiB per-container limit. Sampling occurred at different times; these figures do not replace the original StageD baseline. Two original StageD containers also remained running: four total active containers, without a four- or five-container load benchmark. Guest MemAvailable after the test was **3,982,995,456bytes (~3.71GiB)**, above the2GiB reserve.

Model V2309A, brand vivo, device PD2309 and the sourced China fingerprint matched via getprop in both instances. Synthetic serial and persist.radio.imei values were populated, distinct and stable across restarts. The telephony Binder probe returned no usable IMEI; property injection does not establish modem/TelephonyManager identity support. Actual OS remains Android13/SDK33; the sourced fingerprint describes China Android16 firmware. See [STAGE_E_IDENTITY.md](STAGE_E_IDENTITY.md).
