# SimuFarm status — 27 October 2026

Organization: simufarm-team. Repository: simufarm. Monthly ceiling: US$200.
Provider: provisional Hetzner dedicated Server Auction policy, exact SKU and all-in quote unverified (ADR 009).

| Milestone | Progress | Completion evidence / blocker | Next task |
|---|---:|---|---|
| Initial five actions | 100% of local artifacts | Scaffold, ADRs, contracts, tasks, 1,000-target proposal and report delivered; approval pending | Human target review |
| P0 Bootstrap | 70% engineering estimate | Local code/checks pass; Docker deployment, Python 3.12/Node 22 CI, registry publication and remote review outstanding | P0-bootstrap |
| P1 Static pipeline | 0% of DoD | No verified profiles; generic shell primitive only | P1-generator after dependency resolution |
| P2 Profile extraction | 0% | Explicit target approval required; external agents not connected | P2-gemini-extract after approval |
| P3 Interactive simulators | 0% | Not started; mock chrome and device pages absent | Scope after verified data |
| P4 Emulator farm | 0% | Not started; KVM host and paid resource approval absent | P4-emulator-spinup |
| P5 App testing | 0% | No Appium/APK runs, result API or report UI | Define sample APK and native harness |
| P6 Scale | 0% | No benchmarks, audit, autoscaling or unit-cost measurements | Post-MVP only |

Percentages are not a claim of global DoD. The 70% P0 value estimates preparation effort, not production readiness. No PR was merged and no remote CI run occurred.

## Current evidence
- 19 pytest checks pass, including API integration and safety/data-contract rules.
- One Playwright browser smoke test passes.
- Ruff, generated-contract drift checks, TypeScript validation and Vite production build pass.
- Target checks: exactly 1,000 unique proposals, source URLs present, no approved real profiles.
- Six task/service YAML documents parse. Docker Compose runtime/config semantics not verified with Docker.
- npm dependency audit at installation reported zero known vulnerabilities.
- Host runtime: Python 3.14.6, Node 26.4.0; target-runtime checks remain pending.
- A FastAPI/Starlette TestClient httpx deprecation warning remains; tests pass.

## Counters
Approved profiles 0; proposed targets 1,000; live static URLs 0; interactive simulators 0; functional Android instances 0; cloud resources purchased 0.

## Next actions and blockers
1. Review and approve or revise _targets.yaml; define intended phones/tablets/regions and iOS visual coverage. Clarify 'top 200 brands'.
2. Finish P0 on a Docker-capable host and GitHub repository; approve registry/publication destination.
3. Resolve P1/P2 dependency ordering with the human operator before extraction, using ADR 007.
4. Establish field-evidence validation and a human review workflow before promoting extracted profiles.
5. Dispatch task files manually to external agents, or approve/configure explicit integrations later.
6. Confirm a real KVM host, final quote and cost approval before P4.

See EXECUTION_REPORT.md for the complete delivery report and docs/WEEKLY_SUMMARY.md for costs and risks.
