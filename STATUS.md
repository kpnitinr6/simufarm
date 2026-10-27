# SimuFarm v3 status — 27 October 2026

Stage A accepted and merged. Stage B static DoD accepted by the operator: 20 shells, 20 templates, 22 profiles/pages, 52 Python tests, 16 browser tests and green Python 3.12 / Node 22 CI. Vivo backfill is deferred to an independent runtime-evidence track and does not block Stage C. Stage C is authorized; planning has begun, generated cohort count is currently 0/1,000. Generator implementation is pending and must explicitly emit build: null and runtime_eligible: false. Stage D is preparation only until Stage C acceptance.

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

New runtime evidence task: tasks/vivo-build-property-evidence.yaml, assigned to local DeepSeek. Y100 extraction paused needs-human for region resolution. X100 candidate regional mismatch must be reviewed; third-party/firmware-dump source classes remain candidate evidence until schema support and human promotion. No resources provisioned.
