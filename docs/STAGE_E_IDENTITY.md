# Stage E identity injection — 2 November 2026

The requested local two-container **getprop identity test passed**, including persistence across a container restart. Stage D was accepted by the user. This implementation is awaiting code review and general runtime-profile promotion is still pending.

## Implementation

The isolated Docker environment probe retained `-e` properties in Docker Config.Env, but Android returned the default Redroid model/brand and empty serial/IMEI properties. Its stopped container and raw evidence were retained.

The fallback image derives from the immutable StageD Redroid13 ARM64 64-only digest. Official Magisk v31.1 APK SHA256 is verified before extracting its ARM64 binary; the binary digest is also checked. Only the standalone resetprop applet is used. The image bakes an Android init script which executes synchronously immediately after `load_persist_props`, before zygote starts. It reads a read-only per-instance property file and applies `magisk resetprop -n -f`. The image retains Android `/init` as PID1. It does not install a Magisk manager, root daemon or unrestricted sudo policy.

`infra/redroid-identity/toolchain.json` pins the base/tool hashes. The base init file is preserved with the one explicit boot-hook insertion; its original SHA is recorded. The Dockerfile supports the VM's existing legacy Docker builder. The first image-build attempt failed because COPY --chmod requires BuildKit; it created no StageE containers. The compatible retry succeeded.

## China build evidence

The new experimental test profile is `data/runtime-test-profiles/vivo-x100-china.json`, separate from the India reference and production catalog. It has a complete build block but remains `runtime_eligible:false`, with no fabricated human reviewer.

| Property | Test value | Evidence |
|---|---|---|
| ro.product.model | V2309A | [Vivo China X100 specifications](https://www.vivo.com.cn/vivo/param/x100), model listing |
| ro.product.brand | vivo | [V2309A device database record](https://deviceinfohw.ru/devices/item.php?item=120403), BRAND label; firmware fingerprint corroborates brand |
| ro.product.device | PD2309 | [China OTA metadata](../data/research/stage-e-x100-china/ota-metadata.txt), line16 pre-device |
| ro.build.fingerprint | vivo/PD2309/PD2309:16/BP2A.250605.031.A3/compiler260818110530:user/release-keys | Same metadata, line8 post-build |

Primary firmware URL, retrieval method, field confidence, discovery commit and hashes are in `data/research/stage-e-x100-china/provenance.json`. Only bounded ranges were read from Vivo's HTTPS CDN. ZIP metadata CRC was checked; the full10GB package and its cryptographic signature were not verified. The manufacturer model and OTA device family agree with the database record. This is a sourced test candidate awaiting human build-block review.

**Actual OS remains Android13, SDK33.** The available China firmware fingerprint describes Android16. Applying it does not install OriginOS, change Android APIs, reproduce Vivo hardware, or establish a coherent physical-device attestation identity.

## Observed pair

Run: `a0bbed5eefa24c1ea54f936cc207c1e7`; UTC12:01:47–12:02:57. Derived local image ID: `sha256:b5615825294060e4fa4d3a3f4fe2f8a5d26d005f7c7ed37ff65add691fffd53d`.

| Observation | Instance1 | Instance2 |
|---|---|---|
| Container | simufarm-stage-e-a0bbed5eefa2-1 | simufarm-stage-e-a0bbed5eefa2-2 |
| Guest-loopback ADB | 127.0.0.1:5561 | 127.0.0.1:5562 |
| First boot | 9.183s | 12.761s |
| Restart boot | 9.133s | 10.287s |
| First RAM sample | 636.5MiB | 645.4MiB |
| After-restart RAM sample | 667MiB | 681.9MiB |
| Requested six getprops match | Yes | Yes |
| Boot-hook marker | 1 | 1 |
| Serial/IMEI unchanged after restart | Yes | Yes |

Both ro.serialno and persist.radio.imei were nonempty and different between instances. Android IDs also differed and remained stable on restart. Assigned serials have SFTEST prefixes; IMEIs use synthetic zero-prefix test values with a Luhn check digit. They are not claimed to be allocated physical-phone identifiers. Raw values remain in local evidence.

The separate `service call iphonesubinfo 1` probe returned `Parcel(fffffffc ffffffff 00000000 ...)`, not a usable IMEI. This is retained as an inconclusive/exception service result. No claim is made that TelephonyManager or a radio HAL exposes the injected property. Supporting application-level telephony identity requires its own interface-aware test and implementation.

The pair ran alongside the accepted StageD pair: four running containers total, below the configured ceiling5. Each StageE instance is limited to1200MiB with no extra swap allowance. The runner checks concurrent count and MemAvailable before launches; the post-test guest MemAvailable was3,982,995,456bytes, above the2GiB reserve. These idle boot observations do not constitute a concurrency load benchmark.

## Reproduction

Download the exact official APK URL in toolchain.json. From the clean checkout, run:

```sh
python scripts/stage_e_utm.py \
  --vm-id F28BDEF7-5053-4B12-A98D-A33831B72167 \
  --identity /Users/nitinkarwauth/.ssh/simufarm_stage_d_ed25519 \
  --known-hosts /Volumes/SimuFarmDrive/SimuFarm/evidence/known_hosts
```

This defaults to a plan with no external calls. `--execute-test --magisk-apk /absolute/path/Magisk-v31.1.apk` executes the isolated test through existing UTM guest-agent privileges and strict localhost SSH. It creates two additional instances and refuses execution if that would exceed the five-container ceiling or the memory reserve. With the current four running containers, a new pair will be refused; stop the specifically selected old test pair before rerunning. Do not remove unrelated containers or volumes.

Evidence: workspace `outputs/stage-e-runtime/observations.json`, external drive `SimuFarm/evidence/stage-e/a0bbed5eefa24c1ea54f936cc207c1e7/observations.json`, and the ignored checkout `data/runtime/local/stage-e/`. Prior failed build and environment probe evidence are retained separately. No secrets or VM disks are committed.

## Validation and remaining scope

112 local Python tests passed; Ruff passed. Public remote CI uses Python3.12/Node22; its outcome is recorded in the delivery report. Meaningful new checks cover mixed-region rejection, missing/unsafe properties, synthetic identifier checksums, memory/concurrency limits, pre-zygote ordering, and no-action plan mode.

Remaining: code review; human review of the China build block before catalog runtime promotion; app-level telephony identity support if required; five-container workload benchmarking. The original India reference and all generated draft eligibility flags are unchanged. Zero Oracle API calls, zero MobileAPI calls, zero paid resources created in this work. Oracle cleanup remains a separate unexecuted user-run action.
