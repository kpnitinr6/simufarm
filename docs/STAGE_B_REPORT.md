# Stage B execution report — 27 October 2026

Stage B's static collection is implemented. Stage B is **not complete** because the operator-required full build backfill remains unavailable for all three Vivo devices. PR #2 is a draft, not merged. Stage C has not started.

## Delivered artifacts

- 20 original HTML/CSS/JavaScript Web Component shells: Vivo plus the 19 requested brands. Themes differ in bezel radius, padding, palette, button positions and cutout treatment. These are stylized illustrations, not dimensionally accurate OEM frames or manufacturer UI.
- 20 placeholder profile templates, reserved for the later generator. No Stage C CSV generator or bulk extraction.
- 20 manually researched reference profiles, one per brand; retained Y100/V30 bring the total to 22 sourced drafts and 22 generated static pages.
- Field evidence sidecars and 22 static manifests. A ready static manifest means its preview exists; it does not confer runtime eligibility or human review.
- Generic deterministic static rendering and a catalog with brand filters plus a 20-reference toggle. Existing Vivo URLs remain available.
- Build provenance schema extension with the requested source_type enum and sources URL list. Any asserted build property requires provenance; runtime admission requires all four nonblank values and human review. Generated JSON Schema and TypeScript contracts agree.
- Ten committed frame/art screenshot regression baselines and ten full-page proof screenshots. Text is masked in frame comparisons for cross-platform font stability; these checks do not verify text typography or OEM fidelity.
- ADR 014 approval/addendum recorded. Stage C math corrected to 20 × 50 = 1,000, with 3 OS versions, 2 screen-size classes and 2 chipset families per brand. A shortage for any brand must be reported rather than filled with duplicates.

## Reference cohort

| Brand | Model | Year | Resolution | Android |
|---|---|---:|---|---|
| asus | Zenfone 11 Ultra | 2024 | 1080 × 2400 | 14 |
| Google | Pixel 7 | 2022 | 1080 × 2400 | 13 |
| HONOR | 90 | 2023 | 1200 × 2664 | 13 |
| HUAWEI | P40 | 2020 | 1080 × 2340 | 10 |
| infinix | NOTE 40 | 2024 | 1080 × 2436 | 14 |
| lenovo | Legion Phone Duel 2 | 2021 | 1080 × 2460 | 11 |
| lg | VELVET | 2020 | 1080 × 2460 | 10 |
| Motorola | edge 40 | 2023 | 1080 × 2400 | 13 |
| nokia | G42 5G | 2023 | 720 × 1612 | 13 |
| nothing | Phone (2a) | 2024 | 1084 × 2412 | 14 |
| OnePlus | 11 5G | 2023 | 1440 × 3216 | 13 |
| OPPO | Find X5 | 2022 | 1080 × 2400 | 12 |
| realme | GT 2 | 2022 | 1080 × 2400 | 12 |
| Samsung | Galaxy S21 5G | 2021 | 1080 × 2400 | 11 |
| sony | Xperia 1 VI | 2024 | 1080 × 2340 | 14 |
| tcl | 50 PRO NXTPAPER 5G | 2024 | 1080 × 2460 | 14 |
| tecno | CAMON 30 | 2024 | 1080 × 2436 | 14 |
| vivo | X100 | 2024 | 1260 × 2800 | 14 |
| Xiaomi | 13 | 2023 | 1080 × 2400 | 13 |
| zte | Axon 40 Ultra | 2022 | 1116 × 2480 | 12 |

## Vivo backfill: partial, still blocked

Official India OTA ZIP metadata verified the literal target firmware fingerprints for Y100 and X100. Only a 65,536-byte HTTP range was read from each archive. Raw metadata, hashes, source URLs, range receipts and the AOSP mapping from post-build to ro.build.fingerprint are preserved in data/research/vivo-build-candidates.json.

The installed DeepSeek-R1 8B model ran offline through Ollama. Its X100 extraction matched. Its Y100 extraction changed the compiler suffix and was rejected; the profile uses a deterministic exact source copy. V30 returned null. Model receipts retain the rejected result with an explicit review disposition.

| Device | Verified properties | Missing |
|---|---|---|
| Y100 India | Fingerprint | ro.product.brand, ro.product.model, ro.product.device |
| X100 India | Fingerprint | ro.product.brand, ro.product.model, ro.product.device |
| V30 India | None | All four build properties |

Complete build blocks: **0/3**. Runtime-eligible profiles: **0**. Ten of twelve requested Vivo property values remain unknown. Do not infer model/device/brand from marketing names or fingerprint segments. The outstanding input is matching-device primary firmware/getprop/device-tree evidence for those ten values. No request to approve invented or guessed values is made.

## Validation

Local: 52 Python tests, Ruff, 22-profile field-source validation, schema drift check, TypeScript/Vite build and 16 Playwright tests passed. Ten visual comparisons passed. Catalog and representative full-page screenshots were inspected. Host tools are Python 3.14/Node 26; the public CI specifically validates Python 3.12/Node 22.

Remote CI run [40506761632](https://github.com/kpnitinr6/simufarm/actions/runs/40506761632) passed all checks on commit 77d47c3 using Python 3.12 / Node 22. Recorded job wall time: 66.0 seconds; this is observed elapsed time, not a claim about account-wide billing minutes. The prior Stage A job took 50 seconds. Evidence: data/research/stage-b-ci.json. No Docker/Oracle/runtime validation is claimed or required in this shell-only stage.

## Source caveats awaiting human technical review

All 22 profiles remain drafts; no reviewer identity was fabricated. Region-specific RAM and release dates are recorded in sidecar evidence. Physical screen PPI includes explicitly labeled calculations and is not Android logical densityDpi.

Nothing's manufacturer product and support pages disagree on width (1084 vs 1080); the draft retains the product page value with a conflict flag. Infinix Android 14 uses an explicitly labeled cross-document XOS 14 mapping. TCL detailed specifications use a manufacturer-authored datasheet hosted by Ingram Micro. Huawei's pill-shaped cutout is approximated by the available punch-hole vocabulary. These issues prevent claims of verified hardware fidelity.

## Zero-spend and next gate

Billable resources touched: **0**. Spend: **$0**. Oracle VMs/uptime: 0/0. Containers: 0. MobileAPI calls: 0; actual account remaining unknown, conservative cap 50/month. No paid/trial provisioning, paid model API, model download, deployment, emulator, or runtime image was used. Repository PUBLIC reverified; MOBILEAPI_KEY_STORED=yes remains operator-confirmed without reading the key. Public standard GitHub runners run code/browser checks only.

Remaining: obtain the missing genuine Vivo property evidence, complete full backfills, retain green CI, and receive Stage B acceptance. Only then may Stage C begin. Stage D must re-verify public visibility and free account eligibility before touching Oracle. Runtime boot time/RAM/identity remain unmeasured until their later stage.
