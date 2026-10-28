# Stage C2 remediation and Stage D actuals — 28 October 2026

Stage C engineering is accepted and merged. C2 is implemented for a separate, unmerged review. Stage D is authorized but blocked on authenticated Oracle access and account-specific Always Free allowance checks. Stage E has not begun.

## C2 result: Option B, no padding

The generated cohort is reduced from 1,000 to **933 retained sourced candidate records**, with **67 removed/merged IDs** and no replacement rows. There are 22 retained reference drafts, so 955 static profiles/pages remain. All 933 generated profiles explicitly retain build: null and runtime_eligible: false. Every current profile stores ram_gb as a float.

The earlier assertion of no carrier/cosmetic duplicates was incorrect. C2 records each removal, merge, survivor and source in data/rejections.md and data/research/stage-c2/change-log.json. Generated JSON, evidence sidecars, served profile JSON and page HTML were removed for all 67 inactive IDs. The original dataset importer cannot directly overwrite the curated CSV. Global diversity remains 7 Android versions, 3 screen classes and7chipset families; measured exemptions were regenerated for actual counts rather than padding toward 1,000.

Brand attribution: the two wrongly attributed Xiaomi iQOO entries were removed, as permitted. TCL 10 Tabmid was removed as a tablet. Requested Samsung, Vivo, OnePlus, Xiaomi, TCL and Nokia alias groups were collapsed to stronger supplied sources; additional known spelling/connectivity/cosmetic aliases were removed. When a listed name already had one row, no fictitious duplicate was removed. Stable survivor IDs may retain regional words without adding another catalog entry.

## Verification scope

**105 distinct physical device models have source checks** for exact-model existence, cutout geometry or named corrected fields. That is not a claim that all specifications for 105 or 933 devices are verified. Complete human-reviewed technical/runtime profiles remain 0, and no physical handset was tested. The remaining whole-catalog inherited specs require review. We do not relabel 933 secondary-source candidates as 933 fully verified devices.

The operator approved **100 sourced notch/position checks selected for coverage, with popularity unverified**. Those 100 are applied, with cited reviews or exact-model manufacturer drawings/front renders and explicitly labeled visual inferences. Coverage is 100/933 = 10.72%; 833 remain unknown. Classifications: 23 none, 29 teardrop, 48 punch-hole. No popularity rank was invented. Additional incomplete geometry candidates remain research-only. OEM images were not bundled into the simulator; its art remains original HTML/CSS.

## Specific corrected facts and source conflicts

- Galaxy M44 launch year is 2023; its height is corrected to 2408 pixels using the GSMArena launch report. Xperia 1 IV RAM is 12.0 GB using Sony's launch release.
- The exact Galaxy A53s 5G identity could not be confirmed. Samsung's 2022 release describes A53 5G with Exynos 1280, while the inherited A53s row claimed Snapdragon. The A53s row is quarantined rather than assigning the real A53's year to an unproven identity.
- Official Nothing product pages confirm Phone (4a) and Phone (4a) Pro, so both remain. Samsung's 22 July 2026 launch confirms Fold8 Ultra, so it remains and its screen facts were corrected from the official table.
- Samsung's S25 FE launch table explicitly lists Android 16 / One UI 8. The requested Android 15 correction would contradict that primary source. Android 16 is retained and the conflict is exposed for review.
- Galaxy A83 5G, A75 5G, F64 5G, Z Fold Wide and Realme X9 were not confirmed from qualifying manufacturer/GSMArena sources and were removed. A rumor or unrelated example on a generic support page did not establish existence.

Full source URLs and field scopes are in data/research/stage-c2/SOURCE_CONFLICTS.md and verified-fields.json. A source check is not human promotion.

## Stage D actuals

Separate Stage D readiness PR #4 contains docs/CAPACITY.md, data/runtime/README.md, a bounded Always Free retry adapter and remote diagnostic collector. Its CI is green, but script preparation is not an executed VM benchmark.

| Observation | Actual |
|---|---|
| Provision attempts / VMs created |0/0|
| Containers booted / ADB verified / APK installed |0/0/0|
| /dev/kvm absence or kernel modules |Not observed|
| Boot time / RAM per container |Not measured|
| Four identities differ between two containers |Not tested|
| MobileAPI calls / billable resources / spend |0/0/$0|

OCI CLI 3.95.1 is installed in an isolated Python 3.12.14 environment. The user selected local configuration, but ~/.oci/config is not yet present. Configure it locally; keys/passwords are not sent through chat or committed. Oracle account allowance and deployment parameters still need authenticated checks before a retry loop can run. No paid fallback, trial, provisioning command or image layer pull occurred.

The requested redroid/redroid:13.0.0_64only-latest Linux ARM64 manifest was verified and pinned. The official Appium ApiDemos v6.0.18 release APK was downloaded locally and its SHA256 matched the published GitHub digest. It has not been installed. The collector applies no model identity overrides, boots two fresh-volume diagnostics sequentially, records actuals, and fails on absent/shared IMEI or serial instead of inventing replacements. Build-null diagnostic boot does not promote a runtime profile.

## Gates and checks

Stage E is blocked until C2 is complete/reviewed and >=1 complete human-reviewed runtime-eligible profile exists. Current subset 0. X100 China/India decision remains needs-human. C2 data changes are not merged to main.

Local C2 checks: 84 Python tests and 19 Playwright checks passed, plus source validation, contract drift, frontend build and deterministic generation. Browser checks cover every retained generated page, representative rendering and ten visual snapshots. Remote Python 3.12 / Node 22 CI is recorded after publication.

Zero billable resources touched. Zero MobileAPI calls. Stage D boot, RAM and identity claims remain unmeasured until authenticated execution actually occurs.
