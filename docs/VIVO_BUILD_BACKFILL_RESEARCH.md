# Vivo Stage B build-property source research

Research date: 27 October 2026. Researcher: Codex source helper. This is a source packet for a separately executed local DeepSeek pass; no claim is made that DeepSeek performed this research.

**Updated result: two manufacturer OTA target fingerprints verified; zero complete build blocks.** Y100 and X100 have literal `post-build` metadata values. Their other three requested properties remain unknown, and all four V30 properties remain unknown. No profile file was changed. The candidate packet is `data/research/vivo-build-candidates.json`.

| India target | Primary-source result | Backfill decision |
|---|---|---|
| Y100 (2023) | [India manufacturer update](https://www.vivo.com/in/support/upgradePackageData?id=198) names Y100 and `PD2257F_EX_A_13.0.6.6.W30.V000L1`, dated 26 February 2024 | Official OTA metadata now supplies a target fingerprint; other properties unknown |
| X100 (2024) | [India manufacturer update](https://www.vivo.com/in/support/upgradePackageData?id=214) names X100 and `PD2309F_EX_A_14.0.13.4.W30.V000L1`, dated 26 February 2024 | Official OTA metadata now supplies a target fingerprint; other properties unknown |
| V30 (2024) | [India manufacturer page](https://www.vivo.com/in/products/param/v30) provides Android 14 marketing information | Identity context only; no runtime properties |

A manufacturer update filename/version is not `ro.build.fingerprint`. Its PD prefix also does not prove `ro.product.device`. A marketing brand/model cannot establish the exact casing or value of `ro.product.brand`/`ro.product.model`. No concatenation or reconstruction is permitted.

The [Indonesia V30 package](https://www.vivo.com/id/support/upgradePackageData?id=2648) uses `PD2323F_EX_A_14.0.5.5.W20.V000L1`. It is explicitly rejected for India backfill: neither shared marketing name nor an EX suffix proves the requested market. The [Malaysia X100 Pro package](https://www.vivo.com/my/support/upgradePackageData?id=2617) fails both market and base-model checks.

Community identity tables provided possible V2239, V2308, V2318 and PD names for searching. They are not manufacturer firmware dumps, LineageOS trees, or XDA getprop excerpts, so they are not accepted sources for build values. In particular the shared PD2257F lead does not uniquely identify Y100 rather than an iQOO product. An unrelated public `vivo_2026_dump` is Android 11 and cannot backfill any requested model. A China V2309A user issue and an unlocated-market V2318 application crash report likewise cannot supply these India properties.

The JSON preserves short exact candidate excerpts, URL, allowed source type (`firmware` or `manufacturer_spec`), matching reasoning, rejected matches, and search queries. The initial HTML-only excerpts contain no raw property assignments. The follow-up ZIP metadata excerpts below do establish two target fingerprints, so their official download URLs are now recorded as partial build sources. No system/vendor/product aliases were observed, so no alias-to-canonical transformation was made.

The bounded search covered exact V/PD identifiers with property names, fingerprint strings, GitHub firmware dumps, and XDA getprop combinations. Empty results do not prove nonexistence. Shell GitHub API access failed DNS; browser search remained available. No large firmware was downloaded and no external paid service or MobileAPI call occurred.

Next usable evidence is a small publicly accessible raw build.prop/getprop or device-tree excerpt for the exact India model and firmware, with URL and explicit market provenance. Preserve partition-specific property names if present; do not silently substitute vendor/system fingerprints for the canonical property. An offline model may validate or parse this packet, but cannot turn missing source evidence into a verified value.


## Successful bounded ZIP64 metadata follow-up

Both official download hosts returned HTTP 206 for `Range: bytes=-65536`. Only 65,536 bytes from each multi-gigabyte archive were fetched in this successful pass. The ZIP64 central-directory extra fields supplied actual local-header offsets; the metadata entries already lay inside those tail buffers. Y100 metadata used raw DEFLATE; X100 metadata was stored uncompressed. No complete firmware or payload image was downloaded.

| Target | Exact OTA `post-build` value |
|---|---|
| India Y100 | `vivo/V2239/V2239:13/TP1A.220624.014/compiler07102212:user/release-keys` |
| India X100 | `vivo/V2308/V2308:14/UP1A.231005.007/compiler01232129:user/release-keys` |

The packet contains exact UTF-8 metadata, SHA-256 of metadata bytes and of each 64 KB HTTP response, full download URLs, HTTP status/content-range receipts, and the literal copied target value. Direct India support links establish firmware market provenance. This records the target image fingerprint, not evidence that any physical device or Redroid instance actually runs that build.

The [AOSP OTA generator](https://android.googlesource.com/platform/build/+/0f8fcbe271cad06cb21e0c4602baf35758f4adb1/tools/releasetools/ota_from_target_files) writes `post-build` using `GetBuildProp("ro.build.fingerprint", input_zip)`. This explicit standard metadata mapping supports copying the whole fingerprint verbatim. No fingerprint segment was used to infer `ro.product.brand`, `ro.product.model`, or `ro.product.device`. Although `pre-device` is present, it remains context only in this conservative packet. The earlier incorrect ZIP64-offset attempt produced undecodable bytes and was rejected; those bytes are not evidence.

The remaining blocker is exact raw brand/model/device evidence for Y100 and X100 and all four properties for India V30. No matching public LineageOS/AOSP tree or XDA getprop source was found in the bounded follow-up search. Indonesia V30 firmware remains rejected for India. Stage B cannot claim three complete build blocks on this evidence.

## Offline DeepSeek assignment result
Installed deepseek-r1:8b ran locally through Ollama with no paid API. Per-device receipts are in data/research/deepseek-vivo-extraction.json. X100 fingerprint matched exactly. Y100 model changed the compiler suffix (2212 to 2210); rejected and replaced by a deterministic literal copy from firmware metadata. V30 returned null. Assignment is executed, but full backfill remains blocked: Y100/X100 lack three properties each and V30 lacks all four. No model-generated property enters a profile without literal source verification.
