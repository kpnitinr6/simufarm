# Stage C public market evidence and allocation method

Checked 2026-10-27. This document records source capabilities, not a completed 1,000-model census. No paid API or cloud resource was used.

## What can be ranked honestly

[StatCounter worldwide mobile vendor share](https://gs.statcounter.com/vendor-market-share/mobile/worldwide/) exposed September 2026 values: Samsung 23.52%, Xiaomi 11.06%, Oppo 5.79%, Vivo 5.33%. Apple (30.8%) is outside the Android cohort; Unknown (7.47%) cannot be allocated to a named brand. Its [methodology](https://gs.statcounter.com/faq#methodology) measures website page views. Vendor usage share is neither handset sales share nor a model-level ranking. These observations may inform which brands receive spare quota, but cannot establish the popularity of individual devices. Preserve period, geography and retrieval date; never imply a complete 20-brand table from these six displayed entries.

[Counterpoint's primary 2025 global model report](https://counterpointresearch.com/en/insights/iphone-16-worlds-best-selling-smartphone-in-2025-apple-takes-7-spots-in-top-10-models) supplies genuine sales-based model evidence for a small leading subset: Samsung occupies three of the ten positions and Galaxy A16 5G leads Android. It cannot rank the full 1,000-model Android cohort. Any model rank needs its own published position, measurement period and geography; models absent from a top ten have unknown ranks, not ranks 11 onward.

The [public Google Play supported-device list](https://support.google.com/googleplay/answer/1727131?hl=en) establishes compatibility/certification inventory. The [Play Console device catalog](https://google.play/business/devicecatalog/) describes app-specific installs and other device metrics available in Console. Neither a public compatibility row nor the number of its regional model codes is public installed-base reach. No authenticated operator export was supplied for this task. Do not label compatibility counts or spec-site page order as popularity.

A reproducible coverage sort can use evidenced popularity first, then release date and canonical model name. Its unranked tail must explicitly have popularity_rank=null and ranking_method=coverage_order, with the technical source separate from any market source. This is a proposal requiring operator acceptance if a fully popularity-ranked list remains mandatory; deterministic sorting alone does not meet that requirement.

## Distinct models and feasible quotas

Nothing has an operator-set cap of 11. Its [official product collection](https://intl.nothing.tech/collections/phones) repeats names for storage/color SKUs. Collapse those repetitions. Historical models absent from today's collection require their own archived manufacturer evidence. The cap does not justify inventing an eleventh model if only ten source-complete models are available. CMF is a sub-brand: record its attribution explicitly if included under Nothing.

The nominal starting allocation is 50 per brand except Nothing=11, giving 961; 39 additional source-complete distinct models must be allocated elsewhere. This arithmetic is a target, not observed availability. For every other shortfall below 50, add the shortfall to the redistribution pool. Assign spare slots only to brands with verified unused models, ordered by available vendor-usage evidence and stable brand-name tie-break; skip exhausted brands. Record all final per-brand counts. Never multiply region, carrier, RAM, color or storage variants into separate models merely to fill quota. A distinct 4G/5G model requires independently evidenced product identity/spec differences.

Google, Sony, Asus, Lenovo and LG require an inventory census before asserting that 50 post-2019 distinct phones exist. [LG's own closure announcement](https://www.lg.com/us/newsroom/corporate/lg-to-close-mobile-phone-business-worldwide) dates its mobile-business withdrawal to April 2021; later model names cannot be invented. Pre-2020 exceptions require a row-specific coverage justification and source. Tablets, feature phones and rebranded duplicates do not silently count as distinct Android handsets.

## Exemptions follow measurements

The latest operator decision authorizes actual per-brand diversity exemptions, not a license to assume expected failures. Compute launch-OS versions, manufacturer diagonals (<6, 6–<6.5, >=6.5 inches) and chipset families from the selected rows. File only measured failures in data/devices.csv.exemptions.yaml with brand, constraint, reason, evidence and global diversity measurements. Missing or unknown evidence is not a second chipset family or OS version.

Google's chipset exemption is not automatic: [Google's historical hardware table](https://support.google.com/pixelphone/answer/16043605?hl=en) documents 2020/2021 Snapdragon models; newer Tensor models form another family when independently sourced. Count chipset families consistently across brands, rather than treating each Snapdragon generation as a new family solely to pass validation.

The full cohort must still total exactly 1,000 distinct source-complete profiles and meet three OS versions, two screen classes and two chipset families globally. Exemptions cannot waive these global requirements, fabricate unknown specifications, or waive missing source coverage. If inventory or popularity evidence remains insufficient, report the actual count and unmet criterion while completing the generator; do not claim a completed cohort.
