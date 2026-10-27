# SimuFarm Free-Tier architecture decisions
27 October 2026. This is the active decision register. The replacement master prompt supersedes the $200/month + $100 setup plan. Paid-path ADRs are archived in docs/archive/PAID_PATH_DECISIONS.md. Recurring cloud budget and setup allowance are now **US$0**. No billable provisioning or trial fallback is authorized.

## ADR 001 — Oracle Always Free ARM proposed; provisioning blocked
Oracle A1 is the requested compute candidate. Lack of usable nested KVM is a constraint, not proof that the selected emulator can run. Software graphics rendering is acceptable in principle, but the prescribed unmodified runtime is blocked (ADR 002). Do not assert a 5–15 minute boot time without a successful measurement.

Primary Oracle documentation currently describes 1,500 OCPU-hours/9,000 GB-hours for Free tenancies (equivalent to 2 OCPU/12 GB), not the prompt's assumed 4/24. The larger price-list allowance is associated with paid tenancies. Do not upgrade accounts to obtain it. Account-specific free allocation, home region, capacity, storage, reclamation rules and current usage remain unverified. 200 GB boot/block and 20 GB object/archive are distinct pools; do not combine them as a 20 GB total. Read docs/FREE_TIER_FACT_CHECK.md.

No provisioning until the operator supplies an active Oracle account confirmation, GITHUB_REPO_URL, ZERO_SPEND_CONFIRMED=yes, and a reviewed account-specific plan proving every selected resource non-billable. Unknown cost blocks action. Email alone is not proof of active/free eligibility. No Terraform apply or resource-creation code is enabled.

## ADR 002 — docker-android + GADS requested; compatibility blocked
Keep the requested stack as a candidate only. Upstream docker-android launcher requires /dev/kvm and requests acceleration; its image installs x86_64 Android. Native ARM/no-KVM support is not established. Passing -no-accel or SwiftShader flags does not bypass the launcher's earlier KVM check. Both proposed flags have version/deprecation concerns. Do not publish a nonworking compose file or claim the emulator boots on Oracle ARM.

GADS adopts already-running emulators; a separate lifecycle owner must start/stop them. GADS requires MongoDB even for ephemeral emulator discovery. Its separate hub-ui licensing must be reviewed before redistribution. Do not pretend SQLite replaces GADS MongoDB: SQLite is planned only for SimuFarm queue/test results. No emulator/GADS service is enabled in the local Compose stack. Read docs/EMULATOR_COMPATIBILITY.md. A supported no-cost runtime alternative requires a reviewed deviation ADR before deployment.

## ADR 003 — Device API quota: conservative 50/month, no calls authorized
The prompt's 200-request allowance is not supported by checked provider pricing/signup. Both show 50 free requests/month; a main-page FAQ contradicts this at 1,000. Set a conservative planning ceiling of 50 and require actual account entitlement/remaining quota before any call. Current remaining quota is unknown; project-made API calls are zero. No quota experiment, signup, key request, paid plan or upgrade is authorized.

The first 100 devices still require explicit identity approval. At one detail call/device, at least two 50-call allocations are needed before retries/searches; 200 profiles cannot be promised this month from that API. Cache every permitted response; reserve retries and stop before the confirmed cap. Review reuse/redistribution terms. Scrapers and local Ollama are separate tools; an LLM is not a network scraper. No scraping, external Gemini/DeepSeek calls or model downloads are authorized automatically as 'free'.

## ADR 004 — Public repository standard-runner CI; remote execution blocked
Default to a public GitHub repository and standard runners only. Current public standard-runner CI is free, but larger runners, other storage/services and private quotas can create costs. Current docs say self-hosted Actions usage is free and the announced platform fee was postponed; do not repeat the prompt's obsolete blanket fee claim. Official hosted Android acceleration exists for supported runners, but this project obeys the prompt's restriction: **no Android emulator in CI**. CI only checks code, contracts and web builds. Manual browser smoke has no schedule; deployments are disabled. Confirm repository visibility/account usage before enabling remotely. Existing GitHub auth is invalid and no remote is configured.

## ADR 005 — Schema 0.2.0 and source-specific human review
Required source_type is api|scraper|manual. Generate TS and JSON Schema from canonical Pydantic. This is a breaking field addition from 0.1.0; bump both package ecosystems and dependent apps to 0.2.0. Existing real profiles would need provenance-backed migration; none exist here.

Scraper profiles must retain confidence <0.9 and require human review before promotion. Human-reviewed low-confidence scraper data is allowed by the revised prompt; API/manual data retains the >=0.9 threshold. Confidence is not factual proof. Every source field still needs a URL; a separate field-evidence sidecar and reviewer record are required before real promotion. Functional iOS emulation remains prohibited.

## ADR 006 — One-session design; local SQLite, no farm scale-out
Maximum planned active emulator sessions is1. A future SQLite queue/result store must claim requests atomically, allow one active lease, renew/expire it and handle cancellation/restarts before enabling launches. No queue service or lifecycle implementation is claimed today. GADS runtime/DB remains a separate prerequisite. Catalog definitions do not imply running sessions. Local API+MinIO development Compose contains no PostgreSQL/Redis or emulator service; paid Compose is archived. A VM, MinIO and image layers all count against actual disk/CPU quotas.

## ADR 007 — Option A and preserved scoped approvals
Keep the operator's Option A: separately approve100 specific devices, collect and human-verify sources, generate100 static pages and review20 visual samples, then expand. The old1,000-name list remains approved for static generation only and explicitly not spec extraction. New500-name vendor-share proxy/top100 are proposals, not inherited approval. The operator chose **iPhone only, accept fewer than100**:55 named iPhone candidates remain, no iPads. No device specs have been fetched. P1/P2 do not start from unsupported names/spec guesses.

## ADR 008 — P6 requires paid infrastructure. Not executed.
P6 is out of scope for the free path. No 10,000-device scale-out or1,000 concurrent emulator plan is executed. Reconsidering paid infrastructure requires a new operator instruction, not exhausting a trial/free quota.

## ADR 009 — Zero-spend task gate and blocked work
Every active task records will_create_bill, local/external scope and remaining approval gates. Local code/docs/tests are non-billable infrastructure actions; resource creation, quota-consuming calls and unknown external charges remain blocked. No unknown-cost action is treated as zero-cost. scripts/zero_spend_check.py evaluates declarations and reports only; it is not an executor or an independent billing guarantee. No automatic resource, API or remote CI calls are attached to it. Trials, upgrades, public noVNC/ADB exposure and paid-provider fallback are disabled.

## ADR 010 — Completion evidence and host limitations
Docker CLI/socket, OCI access, target Python 3.12 and usable GitHub authentication are absent. Host checks use Python 3.14/Node 26; intended CI is3.12/22. P0 is not done: no VM exists from this task, no emulator/noVNC boot was observed, and no deployed API was tested. Source research and YAML parsing do not replace runtime evidence. Every milestone additionally requires zero-spend/quota evidence and applicable human approvals.
