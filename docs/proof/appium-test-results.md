# Local ApiDemos Appium test — PASS

Date:2November2026 (India time). **Result:PASS. Execution time:13.631seconds**, including session creation, UI actions, XML/screenshot capture and session deletion. This is the actual test duration, not dependency-install/build time.

## Environment

| Component | Observed |
|---|---|
| Host | Mac Mini, external-drive UTM VM |
| VM | Ubuntu22.04 ARM64,4CPU/8GiB |
| Runtime | Official Redroid14 ARM64 64-only, pinned manifest46478a567194… |
| Profile | Human-reviewed vivo-x100, China V2309A/PD2309 |
| Actual Android / SDK | 14 /34 |
| Fingerprint | vivo/PD2309/PD2309:14/UP1A.231005.007/compiler05201704:user/release-keys |
| GADS | v6.1.0, ARM64 build of d8abfc32e282d872a08484cd6a1e4a535c0cebe9 |
| Appium | 3.9.0, started and owned by GADS provider |
| UiAutomator2 | 8.7.3 |
| GADS Appium plugin | 0.0.13, local pinned source |
| Sample | Official Appium ApiDemos-debug.apk v6.0.18 |
| APK SHA256 | a9eecf37b26cd084855c530db81c2bb1b91f4c1b095a04f47aa7c20e2791f686 |
| Device / system port | VM127.0.0.1:5561 /8201 |
| Appium route during test | Mac14723 SSH tunnel → VM127.0.0.1:41229 |

GADS hub/provider were running at VM-loopback10000/10001; MongoDB was local and memory-limited. The provider reported the virtual Android device live, connected and Appium up. The GADS plugin was active and registered with the provider. The test used that provider-managed Appium server directly, not the GADS grid queue endpoint; grid scheduling/nightly execution is not established by this smoke test.

## Assertions and artifacts

1. Confirm Appium ready and create a UiAutomator2 session for Android14.
2. Launch io.appium.android.apis/.ApiDemos and confirm its package in the XML hierarchy.
3. Locate and click **Views**, **Buttons**, then **Normal** by accessibility ID.
4. Capture the resulting native UI screenshot and XML.
5. Delete the WebDriver session; deletion returned successfully.

- [Machine-readable result](appium/result.json)
- [Native screenshot](appium/screenshot.png)
- [Initial XML](appium/source.xml)
- [XML after actions](appium/source-after-actions.xml)

The screenshot was visually inspected and shows Views/Buttons and its NORMAL control. This is evidence for this sample/sequence only, not a general app-compatibility or real-phone certification claim.

## Setup corrections

The preparation had paired UiAutomator2version9with Appium3; version9requires Appium4. Execution used the compatible8.7.3driver with Appium3.9.0. The official GADS Linux asset is x86-64, so the pinned source was built for ARM64. Its official Swagger-generation step and verified release UI archive were included. The local plugin source required its declared npm dependencies before it could load. A wrapper normalizes the upstream singular plugin flag, enforces loopback binding and captures server logs, while leaving plugin-management CLI arguments untouched.

The test invocation itself passed on the first measured attempt after these setup corrections. No failed setup was relabeled as a passing Appium run.

## Shutdown verification

The session was deleted. GADS provider/Appium and hub received SIGTERM; their owned process groups had no remaining processes. MongoDB stopped with exit0. The first ordinary Docker stop required its timeout after Android data had been synced (exit137, not an OOM). A subsequent Android-aware shutdown was validated in a verified private PID namespace: **2.176s, no Docker-stop fallback, exit130**, matching Linux's namespace-poweroff SIGINT behavior. The VM stayed running and the container data was retained. The owned Mac SSH tunnel was closed. Final inspection confirms no project containers running and no GADS/Appium/MongoDB/ADB listeners. SSH and Docker's infrastructure daemon remain available for the next local developer run.

Zero Oracle API calls, zero MobileAPI calls, zero paid resources touched. No Play Integrity/SafetyNet check was run or claimed.

The final stopped-VM quick-start also passed in326.985s after a bounded early-ADB readiness fix, then its pair shut down without Docker-stop fallback. Final handoff state:0project containers, no automation services, owned host preview/tunnel closed, UTM VM stopped. [Final shutdown evidence](shutdown-result.json).

Public XML line endings are normalized to LF; original raw responses are retained in local evidence.
