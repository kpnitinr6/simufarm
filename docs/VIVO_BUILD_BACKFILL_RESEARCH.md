# Vivo Stage B build-property source research

Research date: 27 October 2026. Researcher: Codex source helper. This is a source packet for a separately executed local DeepSeek pass; no claim is made that DeepSeek performed this research.

**Result: zero verified raw build properties.** All four requested values remain null for India Y100 (2023), X100 (2024), and V30 (2024). No profile file was changed. The candidate packet is `data/research/vivo-build-candidates.json`.

| India target | Primary-source result | Backfill decision |
|---|---|---|
| Y100 (2023) | [India manufacturer update](https://www.vivo.com/in/support/upgradePackageData?id=198) names Y100 and `PD2257F_EX_A_13.0.6.6.W30.V000L1`, dated 26 February 2024 | Package metadata only; no runtime properties |
| X100 (2024) | [India manufacturer update](https://www.vivo.com/in/support/upgradePackageData?id=214) names X100 and `PD2309F_EX_A_14.0.13.4.W30.V000L1`, dated 26 February 2024 | Package metadata only; no runtime properties |
| V30 (2024) | [India manufacturer page](https://www.vivo.com/in/products/param/v30) provides Android 14 marketing information | Identity context only; no runtime properties |

A manufacturer update filename/version is not `ro.build.fingerprint`. Its PD prefix also does not prove `ro.product.device`. A marketing brand/model cannot establish the exact casing or value of `ro.product.brand`/`ro.product.model`. No concatenation or reconstruction is permitted.

The [Indonesia V30 package](https://www.vivo.com/id/support/upgradePackageData?id=2648) uses `PD2323F_EX_A_14.0.5.5.W20.V000L1`. It is explicitly rejected for India backfill: neither shared marketing name nor an EX suffix proves the requested market. The [Malaysia X100 Pro package](https://www.vivo.com/my/support/upgradePackageData?id=2617) fails both market and base-model checks.

Community identity tables provided possible V2239, V2308, V2318 and PD names for searching. They are not manufacturer firmware dumps, LineageOS trees, or XDA getprop excerpts, so they are not accepted sources for build values. In particular the shared PD2257F lead does not uniquely identify Y100 rather than an iQOO product. An unrelated public `vivo_2026_dump` is Android 11 and cannot backfill any requested model. A China V2309A user issue and an unlocated-market V2318 application crash report likewise cannot supply these India properties.

The JSON preserves short exact candidate excerpts, URL, allowed source type (`firmware` or `manufacturer_spec`), matching reasoning, rejected matches, and search queries. No accepted excerpt contains a raw property assignment. `build_sources` therefore remains empty for every model; candidate metadata must not be emitted as verified build evidence. No system/vendor/product aliases were observed, so no alias-to-canonical transformation was made.

The bounded search covered exact V/PD identifiers with property names, fingerprint strings, GitHub firmware dumps, and XDA getprop combinations. Empty results do not prove nonexistence. Shell GitHub API access failed DNS; browser search remained available. No large firmware was downloaded and no external paid service or MobileAPI call occurred.

Next usable evidence is a small publicly accessible raw build.prop/getprop or device-tree excerpt for the exact India model and firmware, with URL and explicit market provenance. Preserve partition-specific property names if present; do not silently substitute vendor/system fingerprints for the canonical property. An offline model may validate or parse this packet, but cannot turn missing source evidence into a verified value.
