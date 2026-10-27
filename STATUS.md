# SimuFarm v3 status — 27 October 2026

Stage A accepted and merged in PR #1. Stage B is authorized and in progress; Stage C is not started. Overall Stage B completion is below 100% because the three complete Vivo build backfills remain blocked. Counts below describe delivered artifacts, not human technical approval.

| Counter | Actual |
|---|---:|
| Original brand shells | 20 / 20 |
| Brand profile templates | 20 / 20 |
| Reference cohort profiles | 20 / 20 |
| Additional retained Stage A profiles | 2 |
| Total sourced draft profiles / static pages | 22 / 22 |
| Human-approved technical profiles | 0 |
| Complete Vivo build blocks | 0 / 3 |
| Firmware-sourced Vivo fingerprints | 2 / 3 |
| Visual regression sample baselines | 10 / 10 |
| Oracle VMs created / managed uptime | 0 / 0 |
| Runtime containers / runtime-eligible profiles | 0 / 0 |
| MobileAPI calls | 0 |
| MobileAPI remaining account quota | Unknown; conservative budget 50/month |
| Billable resources touched / spend | 0 / $0 |
| Emulator boot time / RAM | Unmeasured; Stage D only |

Repository PUBLIC reverified through GitHub on 27 October. MOBILEAPI_KEY_STORED=yes is operator-confirmed; no key was read and no API call authorized or made. Re-verify repository visibility and account-specific nonbillable eligibility before Stage D.

ADR 014 approved with build provenance addendum. Schema rejects asserted build properties without classified sources; runtime requires all four properties and human review. Y100/X100 official firmware supplies fingerprints only. Other three properties per device and all V30 properties remain unknown. Offline DeepSeek assignment executed; a Y100 transcription mismatch was rejected against literal firmware evidence. See docs/VIVO_BUILD_BACKFILL_RESEARCH.md.

Validation: 52 Python tests and 16 browser tests passed locally; Ruff, source validation, contracts and frontend build passed. Remote run 40506761632 on 77d47c3 passed all steps on Python 3.12 / Node 22 (job wall time 66.0 seconds; public standard runner, $0). Final report-only commit may have a separate check. Public standard-runner CI only; CI contains no emulator/cloud deployment. No paid APIs, trials, provisioning, or model downloads. Stage C allocation corrected to 20 × 50 = 1,000, with diversity requirements per brand. No bulk extraction/generator has started.
