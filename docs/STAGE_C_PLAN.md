> Historical engineering plan. C2 Option B supersedes the round-number quota; see data/cohort-policy.json and STATUS.md.

# Stage C — authorized plan

Operator accepted Stage B for static/interactive scope. Runtime evidence is a separate track and does not block Stage C. Interactive behavior is not claimed to be implemented by this acceptance.

1. Extend the profile contract to support build: null and explicit runtime_eligible: false. Update API, renderer, validator and generated TypeScript/JSON Schema together. Existing sourced reference build fragments remain preserved; generated static profiles never inherit them.
2. Implement a deterministic CSV-to-profile generator using the 20 templates. Every generated profile emits build: null and runtime_eligible: false explicitly, regardless of template/input build claims. Runtime promotion is a separate human-reviewed operation, never a generator side effect. Reject unsafe IDs, duplicate IDs, invalid sources and missing required technical fields before writing output; reruns preserve identical bytes and unchanged files.
3. Assemble a sourced popularity proposal and verify 20 brands × 50 distinct model rows = 1,000. Brand market share is not model-level popularity. Record market, ranking method, source URLs, physical PPI derivations and uncertainty. Each brand needs at least 3 OS versions, 2 screen-size classes and 2 chipset families. Define size classes by manufacturer diagonal (<6 inches, 6–<6.5 inches, >=6.5 inches); record chipset family classification. Do not invent rows or duplicate variants to fill a shortage; escalate infeasible brand quotas. Pre-2020 entries need justification. Preserve the earlier 22 reference artifacts separately from the 1,000-profile generated cohort.
4. Generate and validate exactly 1,000 cohort profiles and pages. Test deterministic null/false defaults, malicious/duplicate input rejection, source coverage, per-brand diversity and idempotency. Run Python 3.12 / Node 22 CI and representative browser/snapshot checks. Catalog must distinguish generated drafts from approved runtime profiles.
5. Report actual counts and exceptions for operator acceptance. Stage D execution remains blocked until Stage C is accepted.

## Runtime subset
Only complete, human-reviewed build identities with field-level provenance and consistent region/variant can be tagged runtime_eligible: true or admitted to profiles/runtime/. Validators must prevent directory/tag bypass and reject null/partial/unreviewed identities. Stage E consumes only this subset. Candidate evidence never promotes a profile automatically.

## Zero-spend
Local research/code and public standard CI only. No paid APIs/trials/resources. No MobileAPI calls planned; conservative cap remains 50/month. No provisioning or emulator execution in Stage C.
