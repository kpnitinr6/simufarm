#!/system/bin/sh
# Test-only virtual identities supplied by a read-only per-container mount.
set -eu
/system/bin/magisk resetprop -n -f /simufarm/identity.prop
setprop sys.simufarm.identity.ready 1
