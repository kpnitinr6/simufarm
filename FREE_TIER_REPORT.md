# SimuFarm free-tier prompt execution report
27 October2026, Asia/Kolkata. This report supersedes paid-path reports. The supplied repository is https://github.com/kpnitinr6/simufarm .

## What was executed
The replacement prompt's initial local actions were carried out: revised architecture decisions, updated schema contracts, new task handoffs, zero-spend gates, usage tracking and a source-reviewed free-infrastructure plan. No paid/cloud resource, trial or API extraction was initiated.

The operator supplied an active Oracle account confirmation, GitHub repository URL and ZERO_SPEND_CONFIRMED=yes. The email and local-only credentials are stored in an ignored .env; the email is not embedded in tracked deliverables. This satisfies the requested operator-input step, but not actual Oracle quota/capacity or runtime eligibility evidence.

## Artifacts made or changed

| Artifact | Result |
|---|---|
| DECISIONS.md | Free-path ADRs 001–010; paid ADRs archived |
| packages/device-schema | Version0.2.0; required source_type enum; generated JSON Schema and TS |
| Profile review policy | Scraper confidence<0.9 retained after human review; API/manual>=0.9; human evidence required |
| tasks/P0-oracle-provision.yaml | Resource task blocked by entitlement/compatibility gates |
| tasks/P1-static-generator.yaml | Local generator handoff;100 device pilot and20 visual samples specified |
| tasks/P2-api-extraction.yaml | Account quota/top100 approval required; no calls authorized |
| tasks/P4-single-session-runtime.yaml | Single-session runtime handoff, blocked |
| scripts/zero_spend_check.py | Read-only task-declaration gate; never executes actions or proves billing |
| data/usage/free-tier-usage.json | Honest project usage and unknown account totals |
| infra/docker/compose.yaml | Local API+MinIO+bucket-init definition only; untested with Docker |
| infra/oracle-vm/README.md | Provisioning prerequisites; no Terraform/apply/resources enabled |
| GitHub workflows | Standard runners, manual-only; no emulator, cloud deploy or automatic billing usage |
| docs/FREE_TIER_FACT_CHECK.md | Primary-source quota/billing corrections |
| docs/EMULATOR_COMPATIBILITY.md | Upstream ARM/KVM/GADS blockers and evidence |
| iPhone visual proposal |55 iPhone names only; iPads removed as requested |

Existing tested catalog/API foundations remain. The frontend identifies the zero-spend plan and makes clear that live Android sessions are unavailable. A runtime queue/executor, SQLite result integration, Appium harness and real rendering pipeline have not been implemented.

## Critical findings: the prompt is not viable as written

### Requested emulator does not have a verified Oracle ARM/no-KVM path
Upstream budtmo/docker-android installs an x86_64 guest and checks /dev/kvm before launch. It requests acceleration. Passing extra -no-accel flags cannot bypass that earlier check. SwiftShader supplies graphics rendering, not CPU architecture emulation. Native ARM support and a working software-mode image were not established. No image manifest inspection, container pull or emulator boot was performed.

Therefore P0's required successful boot/noVNC DoD is **blocked**, not a slow-but-working implementation. The brief's5–15 minute boot expectation is unmeasured and is not a guarantee. A supported zero-cost alternative requires a new reviewed ADR before deployment. GADS also requires MongoDB and discovers/adopts running emulators rather than starting/stopping them. A separate lifecycle executor is required. Its hub-ui licensing needs review before redistribution.

### Free quotas differ from the pasted assumptions
Oracle's current Free-only documentation specifies1,500 OCPU-hours/9,000 GB-hours, equivalent to2 OCPU/12 GB; the larger4/24 allowance cannot be assumed for this account. Boot/block200 GB and object/archive20 GB are separate storage pools. Remaining account usage and home-region capacity are unknown. No account upgrade is authorized.

MobileAPI pricing/signup show50 requests/month, while a FAQ conflicts at1,000; checked sources do not support200. The conservative planning cap is50 and actual remaining entitlement must be confirmed. With one detail call/device,100 new devices need at least two monthly allocations before retries/searches, unless a verified permitted alternative changes the plan. No API calls were made and no claim of50 remaining is made.

Current GitHub docs describe standard public runners and self-hosted Actions as free, with the previously announced self-hosted fee postponed. Hosted Android acceleration has an official supported-runner announcement, contrary to the prompt's blanket noKVM claim; this implementation nevertheless obeys its restriction and runs no Android emulator in CI.

All claims and dated primary links are provided in the fact-check and compatibility reports. Published free plans are not proof of account-specific non-billability.

## Repository and zero-spend controls
The supplied repository was inspected read-only and is **PRIVATE**, with no existing branches/commits reported at inspection. GitHub access works with network permission; earlier sandboxed 'invalid token' reporting was not a reliable authentication conclusion. The token cannot read user billing usage, so private included minutes and stop-spend controls remain unknown. Repository visibility was not changed.

Automatic workflow triggers and schedules are disabled. Initial source publication, if successful, uses [skip ci] in addition to manual-only workflows; no remote CI run is claimed. No paid-runner, artifact upload or deployment step is enabled. Future manual dispatch remains blocked until free usage/control evidence is available. Source upload itself does not provision cloud infrastructure.

## Validation and actual counters
Local tests/build validation is recorded in the final validation ledger. The backend/schema/policy suite contains35 passing checks, including required source_type, scraped-confidence review, iOS prohibition, API reads, source proposal integrity, bucket initialization error handling and unknown-cost blocking. These tests do not establish factual profile truth, bucket runtime compatibility, account billing eligibility or emulator boot success.

Local runtime is Python 3.14/Node 26. Intended target runtime remains Python 3.12/Node 22. Target-runtime remote CI has not run. Docker is not installed/available, so local container build, startup and bucket initialization remain unverified. One existing FastAPI/Starlette TestClient deprecation warning is recorded; no test failure resulted.

| Counter | Actual observation |
|---|---|
| New billable infrastructure commitments | $0 |
| Oracle VMs created by this task |0 |
| Project-managed VM uptime |0 |
| MobileAPI authenticated calls by project |0 |
| Account API quota remaining | Unknown |
| GitHub workflows started by this task |0 |
| Private CI minutes remaining | Unknown |
| Approved technical profiles |0 |
| Device-specific generated static pages |0 |
| Emulator sessions / measured boot time |0 / unmeasured |
| noVNC / GADS / Appium runtime verification | Not performed |

This infrastructure figure excludes any pre-existing subscription/session costs; none were measured or newly authorized by this implementation.

## Remaining work
1. Establish a supported zero-cost runtime architecture; the requested upstream ARM/no-KVM combination is blocked. No paid/trial fallback is permitted.
2. Verify Oracle account-specific free resources, remaining quotas, capacity and storage before a reviewed nonbillable resource plan.
3. Obtain a Docker-capable environment; collect actual API/image/bucket evidence and, only after feasibility/approval, Oracle/emulator/noVNC evidence. P0 stays incomplete.
4. Verify private GitHub included minutes and stop-spend controls, or explicitly authorize a public repository change before enabling remote CI. Visibility is not changed automatically.
5. Approve100specific extraction targets and actual source entitlement/reuse terms; then collect specs with cached quota discipline and human evidence. The earlier static-only list does not authorize extraction.
6. Implement100 static renders/20 visual samples,200 reviewed profiles,200interactive pages, single-session queue/lifecycle, GADS/Appium and SQLite test results in later milestones, conditional on actual feasibility and quotas.
7. Keep P6 excluded. No 10,000 device/1,000 concurrent claim is made.

The project is ready for code/architecture review. It is not a deployed free emulator farm, and the research blockers are material feasibility findings rather than completed runtime work.
