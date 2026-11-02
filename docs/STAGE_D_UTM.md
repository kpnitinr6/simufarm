# Local UTM Stage D — external drive

The user confirmed the2TB Seagate One Touch disk. Immediately before erasing, macOS reported external/physical,2000398933504bytes, /dev/disk7, One Touch w/PW. It was formatted APFS as SimuFarmDrive. The1TBdisk6 was untouched. Disk identifiers can change after reconnecting; never reuse disk7 as a future erase target without fresh confirmation.

UTM5.0.8 was installed from Homebrew. The ARM64 Mac has16GB RAM. UTM's QEMU/HVF VM is configured for4CPU and8192MiB RAM with a128GiB sparse QCOW2 disk physically on the external drive:

`/Volumes/SimuFarmDrive/SimuFarm/VMs/SimuFarm.utm/`

The UTM UI explicitly shows this external path and localhost-only TCP2222 forwarding to guest22. Ubuntu22.04.5 ARM64 live-server ISO was downloaded from Canonical and verified against published SHA256 `eafec62cfe760c30cac43f446463e628fada468c2de2f14e0e2bc27295187505`. Installer, seed ISO, boot kernel/initrd and virtual disk all reside on the external drive. No raw physical disk is attached to the guest.

Unattended installation uses a CIDATA seed and extracted verified ISO kernel/initrd. Seed contains only the SSH public key and a random hashed password; password SSH is disabled. The account is `simufarm`, with Docker access and sudo for this dedicated test VM. The private SSH key remains on the Mac. Seed/private access material is not committed.

After the installer powers off, remove installer drives and direct kernel/initrd boot arguments from config.plist, reload UTM's configuration, and boot the installed virtual disk using UEFI. Do not leave autoinstall active on later boots.

## Controller

```sh
python3 scripts/stage_d_local.py --transport utm --host 127.0.0.1 \
  --port 2222 --user simufarm --identity /path/to/local/private-key --preflight
```

UTM mode accepts only127.0.0.1, requires normal SSH host-key verification, and defaults to port2222. Meshnet mode remains separate and cannot silently use loopback. Optional `--known-hosts` supplies a dedicated verified host-key file. The controller performs no cloud calls.

Use the existing collector to boot two independent Redroid containers only after Ubuntu, Docker, binder/ashmem, APK checksum and immutable ARM64 image are verified. ADB remains bound to loopback inside the VM. KVM is optional. Keep missing/identical identity values visible; no spoofed serial/IMEI is substituted. Record actual boot/RAM observations, even if the complete four-field identity gate fails. Do not promote a profile or begin StageE.

Run evidence and installer serial logs are stored under `/Volumes/SimuFarmDrive/SimuFarm/evidence/`. Actual installation/runtime results belong in docs/CAPACITY.md only after observed; creating this configuration alone does not establish installation or StageD success. Oracle remains disabled by config/stage-d-target.json. Zero Oracle/MobileAPI calls for this setup.

## Installer recovery

First installation failed at the optional `linux-modules-extra-generic` download step (exit100). A PTY logger also echoed guest output back into the console; it was replaced by a read-only TCP serial logger that sends no input. A proposed Ctrl-C diagnostic was rejected by automatic review and was not executed. After logs established that installation had failed, a normal guest shutdown was requested, the stopped state was verified, and the failed virtual disk was preserved under evidence/failed-install.qcow2. A fresh sparse virtual disk and revised seed retry the install without the failing metapackage. The physical external drive was not reformatted again. Install exact kernel modules only after inspecting the installed guest.
