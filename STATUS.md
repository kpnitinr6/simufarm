# SimuFarm status — Stage C implementation, 27 October 2026

Stage A and Stage B static scope accepted; Stage B merged in PR #2. Stage C implementation is delivered for review. Static generation target: **100% (1,000/1,000 profiles and pages)**, plus 22 preserved reference drafts/pages. Overall Stage C acceptance remains pending. The cohort is a sourced secondary-data static draft, not 1,000 independently manufacturer-verified specifications. Model-level popularity rank coverage is 0/1,000; deterministic coverage/release-recency selection is disclosed and needs operator acceptance against the original popularity requirement. No Stage D execution.

All **1,000 generated profiles explicitly serialize build: null and runtime_eligible: false**. Tests inspect every real generated file and compare CSV identities/counts. Human-approved runtime profiles: 0. Approved runtime directory admissions: 0. Earlier Vivo partial build evidence remains in the separate reference/evidence track.

## Actual generated counts and diversity

| Brand | Profiles | Android versions | Screen-size classes | Chipset families |
|---|---:|---:|---:|---:|
| vivo | 64 | 4 | 2 | 4 |
| samsung | 64 | 6 | 2 | 4 |
| xiaomi | 64 | 5 | 2 | 4 |
| oppo | 64 | 4 | 2 | 3 |
| realme | 64 | 6 | 2 | 4 |
| oneplus | 64 | 6 | 2 | 3 |
| google | 24 | 7 | 3 | 2 |
| motorola | 64 | 6 | 2 | 4 |
| honor | 64 | 5 | 2 | 3 |
| huawei | 55 | 5 | 3 | 4 |
| nokia | 60 | 4 | 3 | 3 |
| sony | 20 | 6 | 3 | 2 |
| asus | 27 | 6 | 2 | 2 |
| lenovo | 15 | 3 | 1 | 3 |
| lg | 23 | 1 | 3 | 2 |
| tecno | 64 | 7 | 2 | 3 |
| infinix | 64 | 6 | 2 | 3 |
| nothing | 11 | 5 | 1 | 2 |
| zte | 64 | 7 | 2 | 4 |
| tcl | 61 | 6 | 3 | 4 |
| **Total** | **1,000** | **7 global** | **3 global** | **7 global** |

Nothing-company count 11 includes nine Nothing phones and two explicitly disclosed CMF models; no cosmetic Community Edition or RAM/carrier variants pad the quota. If the operator requires the Nothing brand alone, that leaves a two-model shortfall and needs a quota decision, not invented devices.

Global mandatory minima (3 OS versions / 2 sizes / 2 chipset families) pass. Observed Android versions10–16; seven normalized chipset families. Size classes: <6 inches, 6–<6.5 inches, >=6.5 inches.

## Exemptions filed

23 measured entries in data/devices.csv.exemptions.yaml: quota redistribution for all20brands plus three diversity exceptions:
- Lenovo: 1 screen-size class (large).
- LG: 1 Android version (10).
- Nothing-company: 1 screen-size class (large).

Each entry includes brand, constraint, reason and actual global diversity preserved. No blanket exemptions were applied to Google, Sony, TCL, Tecno, Infinix or HONOR when the actual source cohort passed. Unknown chipset placeholders and spelling duplicates are rejected.

## Validation and zero-spend counters

Local validation: **76 Python tests, 19 Playwright tests**, Ruff, contract drift, 1,022-profile source validation, frontend build and two-run idempotency checks pass. All 1,000 generated URLs served HTTP200 and expected shell/static warnings; five brands were browser-rendered and ten existing visual snapshots passed. Remote Python 3.12 / Node 22 CI is pending the Stage C PR.

Oracle VMs created 0; VM managed uptime 0; containers 0; boot time/RAM unmeasured; MobileAPI calls 0; conservative cap 50/month, actual account remaining unknown. Billable resources touched 0; spend **$0**. No paid API, provisioning, trial or runtime image pull. Repository public standard-runner CI only.

Contract 0.4.0 includes third_party_device_db and firmware_dump and rejects incomplete/unreviewed runtime promotion. X100 China/India choice is needs-human in the runtime task. Separate DeepSeek evidence commit 25848cb is candidate-only; Y100 additional extraction remains paused. Stage D task remains prepared-not-authorized and includes X100 region confirmation before Stage E.
