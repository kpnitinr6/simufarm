# Decision update report — 27 October 2026

## Delivered

ADRs 007 and 009 now implement the operator's decisions. Option A sequences a separately approved 100-device extraction pilot, human verification, 100 static renders and later expansion. The original 1,000 names are approved for static generation only, with specification extraction explicitly disallowed. That approval is now machine-readable and is protected against accidental overwrite by the proposal regeneration script.

The budget is $200 recurring per month plus $100 eligible one-time setup in month 1. The $300 first-month maximum does not permit $300/month recurring spending. No provisioning is authorized before fully green P0 plus a confirmed all-in Hetzner quote including VAT, IPv4, exact configuration and stock.

## Alternative target deliverables

| Artifact | Contents | Limitation |
|---|---|---|
| data/proposals/popularity-targets.yaml | 500 Android candidates, sourced vendor-share weighting | Not a model-level popularity ranking |
| data/proposals/android-top100-pilot.yaml | Separate 100-device Option A review cohort | Pending explicit approval; extraction disabled |
| data/proposals/ios-visual-targets.yaml | 55 iPhone +45 iPad names from Apple | iPad scope pending approval; no comprehensive popularity ranks |

The Android proposal uses September 2026 worldwide Statcounter sampled mobile web-usage vendor shares. It allocates 257 Samsung, 121 Xiaomi, 64 OPPO and 58 vivo candidates. Model-level reach is unknown. Within-vendor editorial ordering is not presented as empirical popularity. An authorized Play Console export or comparable model-level dataset would be required to deliver the requested true model-popularity ranking. See docs/POPULARITY_PROPOSAL.md for methodology and sources.

The Apple proposal contains 100 real catalog model names without padding storage/color/region variants. Its 45-iPad extension is explicit because the reviewed Apple iPhone catalog supplies 55 names. If the desired scope is iPhone-only, the proposal has a 45-device shortfall rather than fabricated targets. No full top-100 popularity measurement is claimed. See docs/IOS_VISUAL_PROPOSAL.md.

No specs, dimensions, screens, screenshots or branded assets were extracted. No list approval was transferred to a new proposal. The operator was asked to confirm the extraction cohort boundary, iPad scope and billing tax/region details; pending answers do not constitute approval.

## P0 engineering changes and actual validation state

Prepared a Compose-integrated API image, local-only idempotent MinIO initializer, dependency ordering and API/Postgres/Redis/S3 write/read/delete verification. Added a Docker smoke CI job with evidence capture, while retaining Python 3.12/Node 22 code checks. Added unit tests for bucket creation, repeat initialization and error handling; these mocks do not prove MinIO runtime compatibility.

**P0 is not Docker-validated and remains incomplete.** No Docker CLI or socket is available in the current environment. No Git remote is configured and the existing GitHub token is invalid. No Docker-capable remote environment has yet been supplied. Consequently compose startup, image build, real bucket initialization and remote CI have not run. The exact runbook is docs/P0_VALIDATION.md and state is recorded in data/validation/p0-state.json. No success is inferred from configuration files.

## Hosting comparison and cost re-estimate

Prepared docs/HOSTING_COMPARISON.md and a machine-readable source ledger. It compares Hetzner AX42-1, OVH RISE-S, Scaleway EM-A610R and AWS m7i.metal-24xl. Provider documentation supports KVM/hypervisor use, but no exact host /dev/kvm or emulator boot test has been performed. Published prices are not confirmed checkout quotes. Account tax status, region, payable currency and stock remain missing.

Hetzner's published AX42 reference is $119/month including primary IPv4 before tax, plus $59 setup before tax. ADR 009 shows illustrative 18%/20% tax scenarios and separate recurring/setup limits; the comparison also shows a 19% example. These are labeled scenarios, not assertions about the user's tax treatment. All calculations must be replaced by a confirmed applicable quote before provisioning.

The comparison flags OVH availability, Scaleway's setup-fee documentation conflict and AWS's far-higher on-demand recurring cost. It does not silently choose or provision a different provider. The operator's Hetzner-quote gate remains binding.

## Remaining external requirements

1. A Docker-capable environment and valid repository/remote-CI access to execute P0 acceptance.
2. An explicit identity-approved top-100 extraction cohort, consistent with the original-list extraction prohibition.
3. iPhone-only versus iPhone+iPad scope confirmation; model-reach data if a measured device popularity ranking is required.
4. Billing country/tax status, acceptable region and a confirmed all-in Hetzner quote with stock. No provisioning until both P0 and quote gates pass.

The source archive is refreshed with this update. No paid infrastructure was created.
