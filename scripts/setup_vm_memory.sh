#!/usr/bin/env bash
# One-time persistent setup, inside the dedicated Ubuntu VM.
set -euo pipefail
export PATH=/usr/sbin:/usr/bin:/sbin:/bin

if (( EUID != 0 )); then
    echo "ERROR: Run this setup as root: sudo bash scripts/setup_vm_memory.sh" >&2
    echo "If sudo is not configured yet, use the VM's root console/root shell first." >&2
    exit 1
fi
if (( $# != 0 )); then
    echo "Usage: sudo bash scripts/setup_vm_memory.sh" >&2
    exit 64
fi
if [[ $(uname -s) != Linux ]]; then
    echo "ERROR: Run this inside the Linux VM, not on the Mac host." >&2
    exit 1
fi
for tool in visudo getent runuser sudo install mktemp chmod chown cp mv rm timeout sync; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "ERROR: Required system tool is missing: $tool" >&2
        exit 1
    fi
done
if ! getent passwd simufarm >/dev/null; then
    echo "ERROR: The simufarm account does not exist in this VM." >&2
    exit 1
fi
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ ! -f "$script_dir/simufarm-drop-caches" ]]; then
    echo "ERROR: Pull the complete repository; the cache helper is missing." >&2
    exit 1
fi
readonly RULE='simufarm ALL=(ALL) NOPASSWD: ALL'
readonly policy=/etc/sudoers.d/simufarm-cache
if [[ -L "$policy" ]]; then
    echo "ERROR: Refusing to replace a symlink at $policy" >&2
    exit 1
fi
# Refuse to layer this change on an already invalid sudoers configuration.
visudo -c >/dev/null
install -d -o root -g root -m 0755 /etc/sudoers.d /usr/local/sbin
candidate=$(mktemp /etc/sudoers.d/.simufarm-cache.new.XXXXXX)
backup=''
changed=0
cleanup() {
    status=$?
    trap - EXIT
    if (( status != 0 && changed == 1 )); then
        if [[ -n "$backup" ]]; then
            mv -f -- "$backup" "$policy"
        else
            rm -f -- "$policy"
        fi
        echo "ERROR: Setup verification failed; previous sudoers policy restored." >&2
    fi
    rm -f -- "$candidate"
    if [[ -n "$backup" ]]; then rm -f -- "$backup"; fi
    exit "$status"
}
trap cleanup EXIT
printf '%s\n' "$RULE" > "$candidate"
chown root:root "$candidate"
chmod 0440 "$candidate"
visudo -cf "$candidate" >/dev/null
if [[ -e "$policy" ]]; then
    backup=$(mktemp /etc/sudoers.d/.simufarm-cache.backup.XXXXXX)
    cp -p -- "$policy" "$backup"
fi
install -o root -g root -m 0755 "$script_dir/simufarm-drop-caches" /usr/local/sbin/simufarm-drop-caches
# Atomic replacement leaves no partially written active sudo rule.
mv -f -- "$candidate" "$policy"
changed=1
chmod 0440 "$policy"
visudo -c >/dev/null
# Test a harmless command as the actual user, without a password prompt or cache write.
runuser -u simufarm -- sudo -n /usr/bin/true
printf '%s\n' "Memory setup complete: simufarm has persistent passwordless sudo."
printf '%s\n' "Installed $policy (root:root, 0440) and /usr/local/sbin/simufarm-drop-caches."
printf '%s\n' "No reboot is required; this configuration survives normal VM reboots."
