# SimuFarm status — 28 October 2026

Stage C engineering accepted and merged in PR #3. Stage C2 remediation is implemented for separate review and **not merged**. Option B: no padding to 1,000. The earlier claim of no carrier/cosmetic duplicates was incorrect; 68 records were removed or merged, including the wrongly branded iQOO entries, a tablet, speculative identities and label/retail aliases.

**Source-checked distinct physical device models: 105**, limited to exact-model existence, cutout geometry or specified corrected fields. **Retained sourced candidate records: 932**. It would be inaccurate to call all 932 fully verified devices. Complete human-reviewed technical/runtime profiles: 0. Physical handsets tested: 0 (software-only project). These verification scopes are separate; see data/research/stage-c2/verification-coverage.json.

## Current generated counts

| Brand | Retained candidates | Sourced notch + position |
|---|---:|---:|
| vivo | 58 | 1 |
| samsung | 45 | 5 |
| xiaomi | 57 | 1 |
| oppo | 64 | 0 |
| realme | 63 | 1 |
| oneplus | 50 | 11 |
| google | 24 | 19 |
| motorola | 64 | 2 |
| honor | 64 | 0 |
| huawei | 55 | 0 |
| nokia | 48 | 39 |
| sony | 20 | 13 |
| asus | 27 | 5 |
| lenovo | 15 | 0 |
| lg | 23 | 0 |
| tecno | 64 | 0 |
| infinix | 64 | 0 |
| nothing | 11 | 3 |
| zte | 64 | 0 |
| tcl | 52 | 0 |
| **Total** | **932** | **100** |

22 earlier reference drafts remain separate; total static profiles/pages 954. Every generated profile has build: null and runtime_eligible: false. All current profile ram_gb JSON values are floats. No replacement rows were added.

Notch coverage: **100/932 (10.73%)**; 832 remain unknown. The operator approved a sourced coverage sample with popularity unverified, replacing the unavailable popularity top 100 for this task. Known geometry includes 23 none, 29 teardrop, 48 punch-hole classifications; visual inferences are labeled and all remain human-review pending. No model rank was invented.

Global diversity still passes: 7 Android versions, 3 size classes, 7 chipset families. All quota and measured per-brand exceptions were recomputed, including Realme/Lenovo/Nothing screen sizes and LG OS spread. No stale 1,000-count or Nothing-quota gate forces padding; CI checks the committed no-padding policy and actual CSV.

## Requested corrections and source conflicts

- M44 launch year 2023 and screen height 2408; Xperia 1 IV RAM 12.0. A53s exact identity could not be confirmed, so it was removed rather than relabeled as A53.
- Official Nothing pages confirm Phone (4a)/(4a) Pro. Samsung's official 2026 launch confirms Fold8 Ultra. These were retained with cited evidence.
- Samsung's official S25 FE launch explicitly lists Android 16; requested 15 would contradict it. Retained 16, with conflict exposed for review.
- Complete removed/merged-ID audit: data/rejections.md and data/research/stage-c2/change-log.json. Rejected profiles, sidecars and public pages are deleted; curated-source checks prevent silent reimport of the original flawed cohort.

## Stage D actuals — authorized, access blocked

Separate readiness PR #4 is green. OCI CLI 3.95.1 is installed locally (Python 3.12.14), and the official Appium APK matches its published SHA256. Oracle configuration has not been observed; no provisioning call has occurred. Repository PUBLIC reverified 28 October. No credentials were read or published.

| Runtime observation | Actual |
|---|---|
| Provision attempts / VMs created | 0 / 0 |
| Containers booted / ADB / APK installs | 0 / 0 / 0 |
| /dev/kvm absence / kernel support | Not observed |
| Container 1 and 2 boot time / RAM | Not measured |
| android_id / imei / serial / adb_serial uniqueness | Not tested |
| MobileAPI calls | 0 |
| Billable resources touched / spend | 0 / $0 |

Actual-capacity file and runtime collection protocol are in the separate Stage D PR: docs/CAPACITY.md and data/runtime/. A verified image digest and prepared collector do not establish boots or identity uniqueness. Missing/shared IMEI or serial will fail the test without spoofing.

## Stage E gate and validation

Stage E has not begun. The code gate requires C2 completion plus human acceptance and at least 1 complete human-reviewed runtime-eligible profile. Current eligible count 0; human acceptance false. X100 India/China choice remains needs-human; no mixed-region identity was promoted.

Local C2 validation: 84 Python tests, source/profile validation and build pass; 20 browser checks passed across the local suite and targeted geometry check. Remote Python 3.12 / Node 22 CI run 40628511620 passed on 965e2a8; the final evidence/geometry-test commit has separate CI. C2 is held for review; no merge authorized. Zero billable resources and zero MobileAPI calls.
