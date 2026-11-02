# Current Stage D update — 2 November 2026

User-confirmed2TB external Seagate drive formatted APFS as SimuFarmDrive;1TB drive untouched. UTM5.0.8 installed. External128GiB sparse disk,4CPU/8192MiB ARM64 Ubuntu22.04 VM configured, localhost2222→guest22. Official Ubuntu22.04.5 ISO SHA256 and Appium6.0.18 APK SHA256 verified. Unattended installation retry in progress after optional package failure; failed virtual disk preserved. SSH and runtime success are not yet established. See docs/STAGE_D_UTM.md.

Oracle remains disabled; zero Oracle/MobileAPI calls for the UTM setup. StageE has not begun. The previous dated status follows as history.

---

# SimuFarm status — 31 October 2026

**StageD pivoted to local Ubuntu22.04 hardware over Meshnet. Prepared; awaiting server IP and SSH username.** ADR015 is superseded by ADR016. Both Oracle launch scripts are execution-disabled before credentials/API access. No retry runner or sleep inhibitor is present; the monitoring automation was already deleted after the29October halt.

Oracle historical actuals:16launch attempts; final HTTP429; no returned VM OCID. Only free network prerequisites were created. Cleanup commands are provided separately for the user; no cleanup or Oracle API query was executed for this pivot. No paid resources provisioned or MobileAPI calls made.

Local actuals:0server connections,0containers booted,0ADB confirmations,0APK installs; boot time, RAM and identity uniqueness remain unmeasured. Architecture and Redroid image selection are pending hardware preflight. See docs/STAGE_D_LOCAL.md and docs/CAPACITY.md.

C2 engineering was accepted. Seven C2.1 geometry unknowns were accepted as exhausted-source deviations, with no guessed values. Generated-artifact integration from the cloud-conflicted original checkout remains a separate unfinished track; no new complete data-validation claim is made here. Older StageC1000-row status is archived under docs/archive/stage-c-status-2026-10-27.md and is not the current verification claim.

StageE has not begun; human-reviewed runtime-eligible subset remains0. The local hardware pivot does not promote a profile or resolve the X100 region decision.
