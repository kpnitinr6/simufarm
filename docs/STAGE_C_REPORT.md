# Historical Stage C engineering snapshot

This report describes the accepted pre-C2 engineering revision. Its duplicate-free data claim was incorrect. Current no-padding counts, rejections and verification scope are in STATUS.md and data/research/stage-c2/.

# Stage C execution report — 27 October 2026

The static generation pipeline is implemented and the real cohort contains **1,000 profiles plus 1,000 pages**. The 22 earlier reference profiles/pages remain separate, so the catalog serves 1,022 total static previews. Stage C has not been accepted or merged; Stage D remains unexecuted.

## What changed

- Deterministic CSV generator uses 20 brand templates and emits profiles/generated/<brand>/<id>.json plus source evidence. Every generated build is explicitly null and runtime_eligible is explicitly false. Incoming CSV/template identity claims cannot promote runtime eligibility.
- Validation rejects unsafe paths, malformed fields, invalid/absent sources, duplicates including spacing/punctuation aliases, unknown chipset placeholders, collision with reference IDs, missing exemptions, stale output and failure of mandatory global diversity. All rows validate before output writes. Identical reruns preserve bytes and file modification times.
- Contract 0.4.0 adds nullable builds, runtime eligibility and source types third_party_device_db / firmware_dump in Python, JSON Schema and TypeScript. Fixtures and admission tests cover null/incomplete/unreviewed identities. Human review and explicit eligibility are required for runtime manifests; placing an ineligible file in profiles/runtime/ is rejected.
- Unknown notch geometry is explicit unknown/unknown and is omitted from original artwork with a visible explanation. No hardware cutout is invented. All source PPI is physical, not logical density.
- Catalog distinguishes reference and generated cohorts, supports search/brand filters, and renders 24 cards per page instead of instantiating 1,000 shells. Static page source links and data attribution are available on generated pages.
- CI regenerates the real CSV cohort and fails on committed profile/evidence drift before running the remaining checks. No emulator or cloud deployment in CI.

## Cohort and exemptions

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

Total 1,000; global diversity 7 Android versions (10–16), 3 screen classes and 7 chipset families. Measured exemptions: Lenovo screen-size diversity, LG OS-version spread and Nothing screen-size diversity. All 20 quota deviations from 50 are recorded. Nothing-company 11 includes two CMF phones and nine Nothing-branded phones; no cosmetic/RAM/carrier duplicates. This parent-company grouping is disclosed for operator review.

## Source quality and ranking limit

The cohort adapts public GetTechAPI/TechAPI revision db1dea0c38ff07fcf400aa05d8c8e4393348eb25  with immutable per-record links, underlying URLs, raw selected fields and source hashes, plus official Nothing supplements. Data attribution and CC BY-SA 4.0 adaptation terms are retained in data/research/stage-c/ATTRIBUTION.md and exposed with generated page specification data. Original shell artwork is separate.

Source research removed unknown chipsets, aliases, regional/carrier/RAM/cosmetic duplicates, future/non-Android and obvious tablet records, known misdated LG X4 Plus and identified bad candidate records. These filters are useful checks, not independent verification of 1,000 manufacturer facts. Every generated profile remains unreviewed; upstream verified flags were not adopted. No firmware/build values were inferred.

Public vendor market share does not establish model-level popularity for 1,000 Android devices. **No model rank is fabricated.** Current selection is deterministic coverage and release recency. This original popularity requirement remains a scope gap: accept that disclosed selection method or provide suitable model-level reach/ranking evidence before treating Stage C as fully accepted. 

## Runtime evidence and later gates

Runtime task contains a needs-human X100 choice: recommended separate vivo-x100-china plus a matching China fingerprint, or preserve India and find matching India identity evidence. V2309A cannot be combined with the India fingerprint. The separate local DeepSeek candidate track also flags V30 Philippines/Android 15 versus the India/Android 14 reference; no candidate has been promoted. Y100 extraction remains paused pending region resolution.

Stage D task is prepared-not-authorized. It specifies verified ARM64 redroid/*_64only-latest image tags/digests and a reviewed/pinned oci-arm-free-retry plan, but no provisioning command ran. X100 region confirmation is a preflight before Stage E. Stage E consumes only the complete human-reviewed runtime subset, currently 0.

## Verification and actual costs

Local 76 Python tests and 19 Playwright tests pass, including 1,000 HTTP page checks, five representative brand renderings, ten visual snapshot regressions, real-cohort policy/count validation and idempotency. Ruff, schema/type drift, 1,022 profile/source validation, TypeScript and Vite build pass. Host Python 3.14 / Node 26; remote CI passed on Python 3.12 / Node 22: [run 40512173427](https://github.com/kpnitinr6/simufarm/actions/runs/40512173427), commit 04878ce, public standard-runner job elapsed 49 seconds. Evidence is saved in data/validation/stage-c-ci.json. [PR #3](https://github.com/kpnitinr6/simufarm/pull/3) remains draft and unmerged.

Billable resources touched **0**; spend **$0**. Oracle VMs/uptime 0/0; runtime containers 0; MobileAPI calls 0, actual account remaining unknown. No paid model API, trial, deployment, image pull or provisioning. Stage C code and drafts are ready for review; acceptance remains the operator's decision.

Pinned-source importer was rerun separately and reproduced identical CSV bytes (SHA256 e6712a51267d2eceb0b99654b980ca048c3bd8c6222f368b583688482397a7b2).
