# Alternative Android target proposal — 27 October 2026

Prepared 500 distinct vendor/marketing-name candidates in `data/proposals/popularity-targets.yaml` (JSON-compatible YAML). This is a **vendor-popularity-weighted review proposal**, not a measured ranking of 500 individual devices. Model-level reach remains unknown. No specifications were extracted and no approval was inferred from the existing list.

## Evidence and limits

[Statcounter worldwide mobile vendor share, September 2026](https://gs.statcounter.com/vendor-market-share/mobile/worldwide/#monthly-202609-202609-bar) supplies the vendor weights below. [Statcounter methodology](https://gs.statcounter.com/faq) describes sampled web page views, rather than device ownership; its FAQ explicitly says it does not publish device/model/user-agent statistics. September figures are still within its stated 45-day revision period. These shares cannot establish installed-base coverage or a model's popularity.

| Vendor group | Worldwide mobile web usage share | Proposed 500 | Proposed first 100 |
|---|---:|---:|---:|
| Samsung | 23.52% | 257 | 51 |
| Xiaomi | 11.06% | 121 | 24 |
| OPPO | 5.79% | 64 | 13 |
| vivo | 5.33% | 58 | 12 |

The selected vendors total 45.70 percentage points of worldwide mobile page views. That is **not** the reach of the selected models. Apple is excluded from this Android proposal; unknown vendors and the long tail are not redistributed as if observed. Other Android vendors are omitted from this first proxy because only these four Android vendors have directly verified shares in the public summary used here. This creates a deliberate breadth limitation, particularly for Google, Motorola, Honor, Transsion and region-specific markets. Worldwide geography is a proposed default, not an inference from the user's location.

## Reproducible selection

1. Reuse the existing local snapshot of [Google's supported-device CSV](https://storage.googleapis.com/play_public/supported_devices.csv), with its SHA-256 recorded in the YAML. It supplies names and identity codes only; certification-list presence is not reach evidence. The snapshot is not claimed to be a newly downloaded catalog.
2. Match source retail branding to the four vendors; group Redmi and POCO under Xiaomi as an explicit editorial assumption. Statcounter's public summary does not establish the exact attribution of these subbrands.
3. Filter obvious TV, tablet, watch, projector, display and camera labels; retain recognized phone-family names. This name-only filter is not verified phone classification. Preserve source branding, device code and one representative model code; a marketing name may span variants.
4. Normalize vendor weights over the selected 45.70 points. Allocate 500 seats with Hamilton's largest-remainder method.
5. Within each vendor, put manually proposed familiar phone families first when present in the catalog, then sort remaining names alphabetically ignoring case. This tie-break order has **no empirical popularity meaning** and makes no recency claim.
6. Interleave vendors using weighted deficit scheduling: at rank `i`, select the vendor maximizing `i * allocated_count / 500 - already_selected`, excluding exhausted pools. `proposal_rank` is this review order.

The file validates at exactly 500 unique `(vendor, casefold(marketing_name))` pairs. All 500 have `spec_extraction_authorized: false`; all have `model_reach_percent: null`. Name aliases, regional variants and obsolete devices still require human review.

## Option A batch and approval gate

Rows 1–100 are flagged `proposed_top100: true`, offering 51 Samsung, 24 Xiaomi, 13 OPPO and 12 vivo review candidates. Examples at the front include Galaxy A15, Redmi 13C, OPPO A38 and vivo Y17s. This first 100 is proposed for approval, not approved for specification extraction. The earlier 1,000-name list is approved only for P1 static mockups; that approval does not extend to P2 extraction or this alternative.

After explicit approval of 100 specific devices, Option A is: extract and verify specifications for those 100, generate P1 from those verified profiles, then expand in approved batches. No extraction has started.

## What would produce a true model-reach ranking

An authorized Play Console export or another licensed/public model-level dataset is required. [Google's device catalog documentation](https://support.google.com/googleplay/android-developer/answer/7353455?hl=en) places catalog access in Play Console after app upload and explains that a device model is a brand/device pair; marketing names alone do not uniquely determine specifications. No connected Console export was available in this task. Public supported-device names do not supply active-device counts.

A replacement reach export should include observation period, geography, active-device definition, brand/device identity, count or share, and whether it measures all Play devices or one app's audience. Rank on that measured count, deduplicate variants under an agreed identity policy, and recalculate the proposed first 100. Until then, do not describe this deliverable as the world's 500 most popular Android models or claim a coverage percentage.
