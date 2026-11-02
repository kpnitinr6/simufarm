# Local UTM Stage D — external drive

The user confirmed the2TB Seagate One Touch disk. Immediately before erasing, macOS reported external/physical,2000398933504bytes, /dev/disk7, One Touch w/PW. It was formatted APFS as SimuFarmDrive. The1TBdisk6 was untouched. Disk identifiers can change after reconnecting; never reuse disk7 as a future erase target without fresh confirmation.

UTM5.0.8 was installed from Homebrew. The ARM64 Mac has16GB RAM. UTM's QEMU/HVF VM is configured for4CPU and8192MiB RAM with a128GiB sparse QCOW2 disk physically on the external drive:

`/Volumes/SimuFarmDrive/SimuFarm/VMs/SimuFarm.utm/`

The UTM UI explicitly shows this external path and localhost-only TCP2222 forwarding to guest22. Ubuntu22.04.5 ARM64 live-server ISO was downloaded from Canonical and verified against published SHA256 `eafec62cfe760c30cac43f446463e628fada468c2de2f14e0e2bc27295187505`. Installer, seed ISO, boot kernel/initrd and virtual disk all reside on the external drive. No raw physical disk is attached to the guest.

Unattended installation uses a CIDATA seed and extracted verified ISO kernel/initrd. Seed contains only the SSH public key and a random hashed password; password SSH is disabled. The ordinary SSH account is `simufarm`. It has no unrestricted passwordless sudo and was not added to the Docker group. Specific administrative diagnostics run through the already-existing UTM guest-agent channel. The private SSH key remains on the Mac. Seed/private access material is not committed.

After the installer powers off, remove installer drives and direct kernel/initrd boot arguments from config.plist, reload UTM's configuration, and boot the installed virtual disk using UEFI. Do not leave autoinstall active on later boots.

## Controller

```sh
python3 scripts/stage_d_utm.py --vm-id F28BDEF7-5053-4B12-A98D-A33831B72167 \
  --identity /path/to/local/private-key --known-hosts /path/to/verified/known_hosts --preflight
```

The UTM controller combines ordinary SSH on127.0.0.1:2222 for file transfer with the existing UTM guest agent for specific privileged preflight/collector programs. It grants no passwordless sudo or Docker-group membership. UUID input is validated; default mode only prints a plan. It observes explicit guest result markers rather than assuming UTM CLI return means guest completion. Missing markers time out without claiming success. Raw evidence is copied back even when the collector fails.

`stage_d_local.py --transport utm` also supports localhost SSH transport, but its direct SSH execution path requires independently authorized guest permissions; the active setup uses `stage_d_utm.py` instead. Both controllers require strict SSH host-key verification. The host key was retrieved through the trusted local UTM guest-agent channel before SSH access was tested. No cloud calls are made.

Use the existing collector to boot two independent Redroid containers only after Ubuntu, Docker, binder/ashmem, APK checksum and immutable ARM64 image are verified. ADB remains bound to loopback inside the VM. KVM is optional. Keep missing/identical identity values visible; no spoofed serial/IMEI is substituted. Record actual boot/RAM observations, even if the complete four-field identity gate fails. The collector does not promote profiles or authorize StageE. The user subsequently accepted StageD and authorized the isolated StageE property test on2November2026; see STAGE_E_IDENTITY.md.

Run evidence and installer serial logs are stored under `/Volumes/SimuFarmDrive/SimuFarm/evidence/`. Actual installation/runtime results belong in docs/CAPACITY.md only after observed; creating this configuration alone does not establish installation or StageD success. Oracle remains disabled by config/stage-d-target.json. Zero Oracle/MobileAPI calls for this setup.

## Installer recovery

First installation failed at the optional `linux-modules-extra-generic` download step (exit100). A PTY logger also echoed guest output back into the console; it was replaced by a read-only TCP serial logger that sends no input. A proposed Ctrl-C diagnostic was rejected by automatic review and was not executed. After logs established that installation had failed, a normal guest shutdown was requested, the stopped state was verified, and the failed virtual disk was preserved under evidence/failed-install.qcow2. A fresh sparse virtual disk and revised seed retry the install without the failing metapackage. The physical external drive was not reformatted again. Install exact kernel modules only after inspecting the installed guest.

The second installer completed package/security-update stages but its final `usermod` hook failed because this Ubuntu22.04 installer defers identity creation to first boot. The installed disk was snapshotted, all installation media/direct boot arguments were detached, and Ubuntu booted successfully. Normal-user SSH was then verified. A proposed unrestricted passwordless-sudo grant was rejected by automatic review and was NOT executed. The safe deployment path uses existing UTM management privileges for the specific authorized kernel/Docker work; ordinary SSH permissions remain unchanged.

The release APK passed its official SHA256 but Android rejected it with INSTALL_PARSE_FAILED_NO_CERTIFICATES. Its container was stopped, not deleted; first-run evidence remains preserved. The corrected run uses Appium6.0.18's official debug APK, SHA256 a9eecf37b26cd084855c530db81c2bb1b91f4c1b095a04f47aa7c20e2791f686. Separate run paths now produce distinct container namespaces, preventing collisions with retained failed runs. Command-failure stdout/stderr are preserved in observations. No identity values are forced.
