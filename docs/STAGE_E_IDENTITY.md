# Stage E — accepted Android 14 identity injection

The user accepted Stage E and approved promotion of `vivo-x100` after a genuine China Android14 fingerprint matched a real Android14 runtime. That condition passed on2November2026 in two fresh containers and again after restarting each one. `profiles/runtime/vivo-x100.json` is now the first human-reviewed runtime-eligible profile. Its India predecessor is preserved under `data/archive/stage-a-india-x100/`.

## Sourced identity

| Property | Verified value |
|---|---|
| ro.product.model | V2309A |
| ro.product.brand | vivo |
| ro.product.device | PD2309 |
| ro.build.version.release | 14 |
| ro.build.version.sdk | 34 |
| ro.build.fingerprint | vivo/PD2309/PD2309:14/UP1A.231005.007/compiler05201704:user/release-keys |

Model: [Vivo China specifications](https://www.vivo.com.cn/vivo/param/x100). Fingerprint and device: [official China OTA](https://sysupdxdl.vivo.com.cn/upgrade/oem/files/2025052020184564386c61632c49847e2056ab22489809.zip), META-INF/com/android/metadata, literal post-build and pre-device. The version is PD2309_A_14.0.25.13.W10.V000L1. Metadata and field provenance are retained in `data/research/stage-e-x100-china/android14/`. Three bounded read-only queries to Vivo's public OTA service located the update. Only a65536byte range was fetched from the official ZIP; metadata CRC was checked. The full archive digest and package signature were not independently verified. No fingerprint was edited or invented.

The official `redroid/redroid:14.0.0_64only-latest` ARM64 manifest is pinned to `sha256:46478a567194aed24cd0877d4434a9e58b534d4aad30931eb21999a52f2ce131`. Both unmodified base build.prop and actual boot SDK/release were checked. The hook refuses to run unless the runtime already reports14/34; setting a release property does not masquerade as an OS upgrade.

## Boot implementation and actuals

Docker environment properties were ignored by Android in the initial isolated probe. The fallback uses the official Magisk v31.1 standalone resetprop applet, with APK and extracted ARM64 binary hashes in `infra/redroid-identity/toolchain.json`. An init hook runs synchronously immediately after load_persist_props and before zygote. A read-only per-instance property file contains the sourced build identity plus distinct synthetic serial/IMEI values. It includes ro.build.version.release=14. Android /init remains PID1; no Magisk manager, daemon or sudoers grant is installed.

| Observation | Instance1 | Instance2 |
|---|---|---|
| Container | simufarm-stage-e-b6c10f6a90e6-1 | simufarm-stage-e-b6c10f6a90e6-2 |
| Guest-loopback ADB | 127.0.0.1:5561 | 127.0.0.1:5562 |
| First boot | 10.158s | 16.854s |
| Restart boot | 9.424s | 9.254s |
| First RAM sample | 650.6MiB | 619.6MiB |
| After-restart RAM sample | 625.6MiB | 610.5MiB |
| All7 requested properties match | Yes | Yes |
| Actual release / SDK | 14 /34 | 14 /34 |
| Serial and IMEI properties stable on restart | Yes | Yes |

Serials and IMEI properties are populated and different between instances; Android IDs also differ. Identifiers are synthetic test values, not claimed allocated physical-phone identities. Raw values remain in local evidence. The derived image ID is `sha256:605b2d3f881374f70b3791de001f6133eedfbba86f60851fe07e3f7694ff7362`.

The test ran UTC12:58:25–12:59:42. Guest MemAvailable was3,549,794,304bytes afterward, above the2GiB Ubuntu reserve. Four containers remain running: two historical StageD Android13 containers plus the new Android14 pair. The old StageE Android13 pair was stopped and retained; no data volumes were cloned or deleted. Five remains the configured planning ceiling, not a load-tested concurrency guarantee.

The collector returned0. Initial evidence transfer failed on a root-owned build.prop snapshot; only that nonsecret snapshot was made readable and the complete evidence transfer then succeeded. The runner now sets that snapshot's read permission itself. No boot test was repeated merely for the transfer correction.

## Limits and promotion

The telephony Binder probe still returns an exception parcel rather than a usable IMEI. getprop works; SIM registration, calls, SMS, cellular data and radio-HAL dependent operations do not work as on a phone. TelephonyManager identity is not established by writing persist.radio.imei.

Matching Android major release and SDK resolves the specific13/16 mismatch. Redroid is still AOSP-based, not Vivo firmware: OEM APIs, drivers, sensors, certification and attestation are not reproduced. No general application-compatibility guarantee follows from a matched fingerprint.

The user's human review is recorded in `data/reviews/vivo-x100.runtime.json`, applied after the matching runtime passed. Only this profile is promoted. The experimental rehearsal profile remains false, and all generated static drafts retain build:null/runtime_eligible:false.

Historical Android13/Android16 evidence is retained locally and in the earlier commit; it is superseded for the active profile. No Oracle or MobileAPI calls, paid resources, new sudo policy or public ADB exposure occurred.

## Reproduction

`scripts/stage_e_utm.py` defaults to plan-only, with no external calls. Supply the existing VM UUID, SSH key and verified known_hosts file. `--execute-test --magisk-apk /absolute/path/Magisk-v31.1.apk` runs two fresh rehearsal instances with the pinned image and verifies restart persistence. It refuses a pair if doing so exceeds5running containers or the2GiB host reserve. With four currently running, stop the specifically selected old test pair before rerunning. Never remove unrelated containers or volumes.

Local raw evidence: workspace `outputs/stage-e-android14-runtime/observations.json`; external drive `SimuFarm/evidence/stage-e-android14/b6c10f6a90e6476b921b2b20f80643f0/`. The implementation remains in PR9 until CI is confirmed and the authorized merge completes.
