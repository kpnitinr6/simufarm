# SimuFarm v3 decision register

Controlling brief: MASTER_PROMPT.md (v3). It supersedes every previous prompt, ADR and execution report. Pre-v3 documents are archived in docs/archive/pre-v3/. Interrupted pre-v3 uncommitted work was preserved in a named Git stash, not carried into Stage A.

Operator inputs were received: supplied repository, public visibility confirmed by GitHub, Oracle account confirmed active, ZERO_SPEND_CONFIRMED=yes and MOBILEAPI_KEY_STORED=yes. Keys/email are not published. No key/account API call is made. Work occurs on pivot/redroid-shell-first. Do not merge until Stage A evidence and human-required items are reviewed; do not start Stage B before approval.

## ADR 011 — Redroid ARM runtime (v3 supersession)
Redroid ARM64 replaces docker-android. No KVM, physical handsets, paid/trial hosts, per-model images or cloned /data volumes. Host plan2 OCPU / 12 GB Oracle Always Free, subject to later account-specific eligibility/capacity. Stage D owns provisioning, kernel validation, real boots and measurements. No VM or runtime container is needed or created during Stage A. Current runtime ceilings remain unvalidated; do not advertise capacity or identities as proven.

The requested redroid/redroid:12.0.0-arm64 tag must be verified in Stage D. A mutable tag, platform documentation, or old image metadata is not an instance boot. GApps/Magisk licensing and host compatibility remain future validation. Do not deploy or bake brand/model images now.

## ADR 012 — Shell-first copy-paste model
Three separate artifacts: handmade brand shells, sourced profile JSON and shared per-OS runtime images. Stage A builds one original Vivo-style Web Component and three manual India-variant profiles. A minimal deterministic static-page renderer reuses that one shell. Copying generated static assets is allowed; runtime image/data cloning is not. Stage C's CSV profile generator is deliberately not implemented before its gate.

Source profile layout: profiles/vivo/vivo-<model>.json. A draft static catalog is separate from the human-approved API/runtime admission path. Generated preview pages are clearly labeled as original artwork with pending human review. Physical PPI (some values derived) is not claimed as Android logical densityDpi or actual runtime identity.

## ADR 013 — Out-of-scope expansion
No 10,000-device expansion,1,000 concurrent emulators, physical-device farm, functional iOS runtime or paid infrastructure. Later stages must stay within the prompt's strict order, real capacity evidence and zero-spend limits. P6 from earlier briefs is retired.

## ADR 014 — Proposed: honest unknowns for Stage A static-only drafts (needs-human)
Manufacturer specifications do not provide genuine ro.product.model, ro.product.device or ro.build.fingerprint values. Codex is not among the allowed verified_by values and no human has reviewed the facts yet. Do not fabricate firmware fingerprints, reuse example V100 values or claim a human reviewer.

**Proposed on this PR only, pending operator approval:** v0.3.0 retains all requested profile keys, with nullable build properties and nullable paired verified_by/verified_at for explicitly labeled static drafts. Runtime admission requires actual human approval and every build property non-null/nonblank. Strict profile promotion still rejects unreviewed drafts. Source-backed preview generation requires an explicit --allow-draft flag and labels its output. No merge/Stage B begins until this clarification is accepted or replaced with supplied verified values.

The requested dpi field is physical PPI for these static references: X100 452 is manufacturer-stated; Y100 413/V30 453 are calculated from manufacturer diagonal/resolution. Their derivation is recorded, not represented as OEM logical density. Notch classification is a visual inference with review pending. Artwork/bezel geometry is original/stylized, not dimensional hardware fidelity.

## Deferred contradictions — do not silently resolve
- Stage C arithmetic:19×52+11=999, not1,000. Resolve allocation before Stage C.
- Shared per-OS images conflict with the per-brand Magisk baking sentence. Resolve before Stage E; no baking now.
- Fresh data does not prove every IMEI/GSF/advertising ID exists or differs on Redroid. Stage D must record actuals and fail missing/duplicate evidence instead of inventing values.
- binderfs supplies Binder IPC; it does not alone replace ashmem. Exact kernel/memfd choices require Stage D evidence.
