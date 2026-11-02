# SimuFarm status — 2 November 2026

**Stage D ACCEPTED by the user. Stage E requested property-injection test PASSED.** UTM Ubuntu22.04 ARM64 VM:4CPUs/8GiB, external-drive storage, SSH localhost2222, Docker and Binder/ashmem verified. StageD baseline:11.435s/13.374s boot,719.6MiB/757MiB Docker RAM. Configured planning ceiling5 concurrent containers, with2GiB reserved for Ubuntu; five-way load capacity remains unbenchmarked.

StageE: Docker environment values were ignored by Android. A pinned official Magisk resetprop binary now runs synchronously after load_persist_props and before zygote. Two isolated vivo-x100-china test instances matched all six requested/related properties: model V2309A, brand vivo, device PD2309, China fingerprint, serial and persist.radio.imei. Both serials and synthetic IMEIs differ and survive container restarts. First boots9.183s/12.761s; restart9.133s/10.287s. Raw evidence is local; docs/STAGE_E_IDENTITY.md records the reviewable results.

Limits: getprop IMEI passes; the separate telephony Binder probe did not return an IMEI. Actual runtime is Android13/SDK33 while the sourced China fingerprint represents Android16 firmware. Test profile is outside the production catalog, runtime_eligible:false and not human-reviewed. Human-reviewed runtime-eligible subset remains0; the latest authorization permits only this isolated StageE test. General profile admission policy is unchanged. The India X100 reference remains separate.

Oracle launch scripts remain disabled and ADR015 superseded. Zero Oracle/MobileAPI calls and zero paid resources created during this work. Four containers currently run (two accepted StageD plus two StageE); two earlier stopped containers remain for audit. No unrestricted passwordless sudo or Docker-group grant was made; specific privileged VM diagnostics use the existing UTM guest agent.

C2 engineering and seven C2.1 unknown-geometry deviations were previously accepted. Static-data integration from the cloud-conflicted original checkout remains separate; this work makes no new catalog-quality claim. StageE code is in a separate draft PR, pending review; nothing merged by this work.
