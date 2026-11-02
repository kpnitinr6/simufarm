> Superseded for deployment on31October2026. Use [local Meshnet procedure](STAGE_D_LOCAL.md). Oracle launch scripts are disabled; the remaining content is historical Oracle readiness evidence.

# Stage D readiness — 2026-10-28

Stage C engineering is accepted and Stage D is authorized. Execution is blocked on authenticated Oracle access, account-specific free allowance evidence, home-region network/image parameters and a reachable ARM host. No VM or container has been created by this task. Do not confuse prepared scripts with runtime validation.

## Free allocation and provisioning

Oracle's current documentation gives Always Free tenancies **1,500 OCPU-hours and 9,000 GB-hours/month**, equivalent to **2 OCPU / 12 GB**. Resources must be in the tenancy home region. Combined boot/block storage has a 200 GB allowance. The proposed single 50 GB boot volume must fit the remaining aggregate allowance; existing resources and current-month usage must be checked first. Never upgrade to PAYG, use trial credits, create paid fallback shapes, or add load balancers/NAT gateways. [Oracle Always Free resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm).

The reviewed retry reference is [ibrahaimbadri/oci-arm-free-retry at 8de2e4c](https://github.com/ibrahaimbadri/oci-arm-free-retry/tree/8de2e4cef89b453dd00945a89f0811fb323bfd25). Its default launch loop is unbounded and retries unexpected failures. Its diagnostics do not establish remaining free storage/current-month usage. Do not execute upstream unchanged. The minimal local adapter `scripts/stage_d_retry.py` adopts AD rotation/capacity retry, fixes sizing to 2 OCPU / 12 GB / 50 GB, bounds attempts, uses >=60-second delays, backs off on 429, stops on unknown/auth/quota errors, and has no paid fallback. Dry run is default. No upstream code is vendored or invoked.

Before `--execute`, create an untracked private preflight JSON with the required fields documented by the script. Evidence files must cover console Always Free image eligibility, account allowance, **all compartments' aggregate inventory**, monthly usage, and public-repository visibility. Review within one hour. Conservative monthly checks reserve a full 31-day run (1,488 OCPU-hours / 8,928 GB-hours). Config and SSH keys stay outside Git. Live SDK checks validate the home region, subnet and ARM image availability; they supplement rather than replace operator-reviewed allowance evidence. A free label alone does not prove unused allowance. Do not run unattended after the bounded attempt window.

## Image and kernel

The upstream [Redroid documentation](https://github.com/remote-android/redroid-doc#readme) lists `redroid/redroid:13.0.0_64only-latest`, supports ARM64, and requires binder/ashmem functionality. It documents `binder_linux`, `ashmem_linux`, and a memfd alternative. Stage D currently requires both modules; failure to load either stops execution pending a reviewed kernel choice. No automatic kernel install or reboot is performed.

Public Docker Registry V2 manifest inspected on 2026-10-28, **metadata only; no image layers pulled**:

- Tag: `redroid/redroid:13.0.0_64only-latest`
- OCI index: `sha256:5a42a569ee1d7c71796c0385e906cbaa4c3e0a162a56d9f26b29bdb1befac13b`
- Linux ARM64 child: `sha256:c815ac1b1d5bd0a099b74c3e3e0eeea3b32bed8d7ab1f788c20fb74e35891716`
- Metadata endpoint: `https://registry-1.docker.io/v2/redroid/redroid/manifests/13.0.0_64only-latest`

The remote script pulls the immutable ARM64 digest, validates its architecture and records image inspection. Revalidate tag metadata before execution if the tag changes. Redroid is a container runtime; KVM is not part of the documented launch. `/dev/kvm` absence is nevertheless an explicit required observation, not an assumption about the unprovisioned host.

## Runtime measurement protocol

Run `scripts/stage_d_remote.py --help` for required inputs. Supply the existing `profiles/vivo/vivo-x100.json`, a reviewed ARM64-or-universal sample APK and independently verified SHA256, and a new run directory under `data/runtime/`. The script needs explicit `--execute` on Linux ARM64. It launches ONE container, waits for boot, verifies ADB and APK installation, then launches the SECOND. Each gets a fresh named data volume and separate loopback-only ADB endpoint. No profile build property or identity override is applied; this is a runtime smoke test, not promotion of the India/China build candidate.

Measured boot time spans `docker run` through `sys.boot_completed=1`; timings include ADB polling. Memory is sampled for both after container two boots, using Docker memory usage and cgroup-v2 `memory.current` where available. Retain raw properties and IMEI service-call output. All four observed values—`android_id`, IMEI, `ro.serialno`, ADB endpoint serial—must be present and different. A loopback ADB endpoint is a transport identity, distinct from Android's `ro.serialno`. Missing or identical IMEI/serial is a **failed requirement**, never a reason to invent/spoof values. Do not claim success if stock Redroid cannot satisfy this.

Containers and volumes are retained for inspection; explicit cleanup follows evidence collection. ADB must never be exposed publicly. Update CAPACITY.md only from observed files, including failures.

## Stage E gate

Stage E remains blocked until Stage C2 is complete **and** at least one complete, human-reviewed runtime-eligible profile exists. Confirm X100 region decision (China versus India) before Stage E. Stage D smoke testing with `build: null` grants no runtime eligibility.

## Local setup actuals
OCI CLI 3.95.1 was installed in an isolated local Python 3.12.14 environment. The operator selected local OCI configuration. Run `oci setup config` from that environment to create the private `~/.oci/config`; keys are not sent through chat or stored in Git. Configuration has not yet been observed, and no Oracle API provisioning call has been made.

The official [Appium ApiDemos v6.0.18 release](https://github.com/appium/android-apidemos/releases/tag/v6.0.18) APK was downloaded locally. Its SHA256 exactly matches the published GitHub asset digest: `14b40d24c4f129bb1b06dcdf8670c101cc1f55b89cacda4a8e3875e83f7883e8`. It has not been installed on an emulator. Receipt: data/validation/stage-d-local-preflight.json. The binary remains outside tracked source.
