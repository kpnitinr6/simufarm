# SimuFarm final handoff — 2 November 2026

The authorized local closeout is complete: the requested PR4–10stack is integrated into main, the provider-managed Appium sample passed, and test services, containers and the UTM VM were shut down. Final handoff code/docs have their own CI/merge record. Machine-readable counts: [project-inventory.json](project-inventory.json).

## Delivered scope

| Stage | Delivered outcome |
|---|---|
| A/B | Original Vivo proof,20brand shells,20templates and22reference profiles |
| C/C2 | Engineering generator followed by honest no-padding remediation to932static candidates;68records removed/merged |
| D | External-drive Ubuntu22.04 ARM64 UTM runtime; Binder/ashmem/binderfs, ADB and sample APK validated |
| E | Actual Android14/SDK34matched to genuine China X100 fingerprint; distinct synthetic identities stable on restart;1human-reviewed runtime profile |
| F | Shared interactive HTML chrome: status/time, keyboard/text input, rotation and dark mode |
| G | Local GADS/Appium harness prepared and its authorized manual ApiDemos sequence passed |
| H | README/limitations, measured Quick Start, safe shutdown helper, proof artifacts and inventory |

## Exact inventory

**4,289 tracked files**, excluding .git, node_modules/virtualenvs, local logs, APKs and VM disks. **932generated static candidate profiles +22references =954current profiles and954HTML pages**, plus20templates. Only vivo-x100 China is runtime-eligible; the other953current profiles remain static-only. The references are a separate collection and may overlap physical models in the generated cohort;954is not a distinct-device verification claim. Physical handsets tested:0.

The source-checked subset is105models for named existence/geometry/spec fields, not complete verification of all932spec sheets. Cutout coverage100/932; remaining unknowns are not invented. The old duplicate-free assertion was incorrect. No padding was added to restore1,000.

| Brand | Generated static profiles |
|---|---:|
| asus | 27 |
| google | 24 |
| honor | 64 |
| huawei | 55 |
| infinix | 64 |
| lenovo | 15 |
| lg | 23 |
| motorola | 64 |
| nokia | 48 |
| nothing | 11 |
| oneplus | 50 |
| oppo | 64 |
| realme | 63 |
| samsung | 45 |
| sony | 20 |
| tcl | 52 |
| tecno | 64 |
| vivo | 58 |
| xiaomi | 57 |
| zte | 64 |
| **Total** | **932** |

## Local runtime and capacity

Mac Mini16GiB RAM; UTM Ubuntu22.04 ARM64 with4CPU/8GiB and128GiB sparse disk on the external drive. Configured ceiling5Redroid containers,2GiB reserved for Ubuntu. Two-container identity/restart behavior is validated; four idle containers were observed historically. Five-way workload capacity is not benchmarked.

Android14 first boots10.158s/16.854s; restarts9.424s/9.254s; sampled RAM625.6MiB/610.5MiB after restart. Official64-only image digest46478a567194…; full pin/source evidence is in STAGE_E_IDENTITY.md and infra/redroid-identity/toolchain.json. Model V2309A, device PD2309, brand vivo and a literal China Android14 OTA fingerprint remain consistent. The prior India reference is archived separately.

## Executed automation and shutdown

[ApiDemos proof](proof/appium-test-results.md): **PASS,13.631s** on GADS v6.1.0ARM64/Appium3.9.0/UiAutomator2 8.7.3. It launched the sample, clicked Views→Buttons→Normal, captured native screenshot/XML and deleted its session. The server was GADS-provider-managed; a production grid queue was not exercised.

The earlier setup needed generated Swagger docs, local plugin dependencies and a server-only CLI compatibility wrapper. Those corrections are documented and pinned. The first cold-start developer trial revealed a transient ADB shell timeout; Android itself booted, and the controller's readiness loop was corrected without extending its180second boot deadline. The subsequent full stopped-VM trial passed.

[Quick Start](QUICK_START.md): **326.985s (5minutes27seconds)** from a stopped VM through VM startup, SSH readiness, two fresh containers and restart checks. One-time prerequisites and downloads were cached. A separate already-running-VM trial measured99.812s. Fresh Ubuntu installation and large downloads are not included in the under10minute target.

Final state: **0project containers,0automation services, UTM VM stopped**. Appium session closed; provider/Appium/hub process groups stopped; MongoDB exit0; owned host SSH tunnel and web preview closed. Final Redroid shutdown used verified private PID namespaces and no Docker-stop fallback, retaining volumes. The initial ordinary Docker stop's timeout was not hidden; the Android-aware helper was implemented and validated afterward. [Shutdown evidence](proof/shutdown-result.json).

## Main integration and validation

PR4,5,6,7,8and10are merged into main. PR9was already merged into PR8and reached main with it. Conflicts were limited to integration metadata/README decisions; C2data and runtime review gates were preserved and reconciled. No requested PR remains open. The final handoff proof/startup changes are submitted and merged with their own CI record.

Local verification:134Python tests, Ruff and954-profile validation passed; the human/runtime gate passes with1reviewed profile. Integrated main CI passed27browser tests and the production build. Final CI runs Python3.12/Node22 on public standard runners; the delivery report links the final main run. CI runs no Android or provisioning.

## Limitations and future extensions

Cellular/telephony does not function; IMEI is a synthetic getprop test value. Play Integrity/SafetyNet should be treated as failing/unavailable on this uncertified emulated runtime; no live attestation result was claimed. OEM firmware/APIs, physical hardware, DRM/sensors and general app compatibility are not reproduced by a matching fingerprint. HTML chrome is a mock, not Android streaming.

The agreed closeout includes StageG preparation and the passing manual sample. A production lifecycle queue, results API/SQLite and nightly scheduling remain future extensions; none is enabled or represented as complete. Other device profiles require their own evidence and human review before runtime promotion.

Zero Oracle calls, zero MobileAPI calls and zero paid resources touched in this closeout. Oracle launch paths remain disabled. Historical Oracle network cleanup was not queried/executed during this zero-Oracle-call work; do not infer that the cloud account was inspected or emptied. Private keys, credentials, VM disks and raw private logs are outside public Git.
