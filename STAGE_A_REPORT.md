# Stage A — Vivo proof of concept

27 October 2026. Controlling brief: SimuFarm v3 in MASTER_PROMPT.md. Branch: pivot/redroid-shell-first. This report covers Stage A only. Stage B–H have not started; no stage skip is authorized.

## Delivered
- Archived previous controlling prompts, ADRs, reports, alphabetical targets and earlier proposals. Interrupted Redroid-first changes were preserved in Git stash; no runtime work was resumed.
- Added ADR 011 Redroid pivot, ADR 012 shell-first architecture and ADR 013 out-of-scope rules, plus proposed needs-human ADR 014 for honest unknown firmware/reviewer values.
- Updated Python/Pydantic, generated JSON Schema and generated TypeScript packages to 0.3.0, including build, shell_id, base_image_id and revised manifest/runtime naming.
- Built shells/vivo/shell.html, shell.css, shell.js and meta.json. All artwork is original HTML/CSS. One shared Web Component handles the different screen aspect ratios/notches; no manufacturer logo, wallpaper or photograph is redistributed.
- Manually wrote three sourced India-variant profiles: vivo-y100, vivo-x100 and vivo-v30. Each has manufacturer parameter/launch URLs and per-field evidence. Physical PPI calculations/visual notch inferences are explicitly labeled. No MobileAPI request was used.
- Implemented minimal deterministic static generation. Exactly three pages and a three-entry catalog are generated. Repeating generation leaves file contents and modification times unchanged, covered by tests. This is not Stage C's CSV profile generator.
- Rendered and visually inspected proof. Screenshots: docs/proof/vivo-y100.png, vivo-x100.png, vivo-v30.png. Additional catalog proof: docs/proof/catalog.png. Mobile overflow also checked.
- Preserved existing safety/test scenarios while migrating their fixtures to the 0.3.0 wire names. Added static-generation and future identity-evidence validation tests. No runtime identifier was created or claimed unique.

## Verification
| Check | Result |
|---|---|
| Backend/schema/unit/integration suite |46 passed |
| Playwright browser suite |5 passed |
| Ruff |Passed |
| Generated-contract drift |Passed |
| Source/field-evidence validation |3 passed with explicit static-draft opt-in |
| TypeScript and Vite production build |Passed |
| Real device/VM/emulator test |Not performed or required for Stage A |
| Remote CI |Recorded in data/validation/stage-a-ci.json once complete |

The local host is Python3.14/Node26. Target CI is Python3.12/Node22. One FastAPI/Starlette TestClient deprecation warning remains without test failures. No broad claim of production readiness follows from these checks.

## Review needed before acceptance/merge
Manufacturer pages do not establish real firmware build properties. The v3 example fingerprint and V100 model string are not used as facts. Build properties stay null, and verified_by/verified_at stay null because no human has reviewed the data and Codex is not an allowed reviewer enum value.

Proposed ADR 014makes those unknowns legal only for explicitly labeled static drafts; runtime admission rejects missing firmware identity and requires real human review. It is a proposed schema clarification requiring approval. Default profile validation still rejects unreviewed promotion; the static generator requires --allow-draft. This PR must not merge until that clarification is accepted or replaced by genuine supplied firmware/review evidence.

The three static pages/catalog/browser proof satisfy the visual Stage A DoD. Engineering artifacts are complete; Stage A human acceptance remains pending. Stage B is blocked until approval. No additional brand shell, bulk CSV extraction, Oracle provisioning, Redroid boot, Magisk, GADS executor or Appium work has begun.

## Real counters / zero-spend check
- New billable infrastructure/resources touched:0.
- Oracle VMs created by this work:0; managed uptime0; existing account usage unknown.
- Running/booted containers:0; boot duration and RAM unmeasured.
- Source profiles3, human-approved profiles0, shared shells1, static pages3.
- MobileAPI calls0; remaining account quota unknown; conservative future cap 50/month. Key existence confirmed by operator; key contents not read.
- Repository PUBLIC already explicitly authorized/verified. CI standard public runners only; no emulators, cloud deploys, paid runners or billable artifact-upload step.
- CI elapsed time/run links recorded from actual runs; account billing minutes are not guessed.

## Remaining stages
B:19 additional shells and20 total brand profiles after approval. C:CSV generator and 1,000 sourced profiles/pages, including corrected allocation math (19×52+11 currently equals 999). D:actual Oracle/Redroid boots/capacity/identity evidence. E:reviewed build override. F:interactive shells. G:GADS/lifecycle/Appium/SQLite results. H:final handoff. No paid or trial fallback.
