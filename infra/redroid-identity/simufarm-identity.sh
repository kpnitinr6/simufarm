#!/system/bin/sh
# Test-only virtual identities supplied by a read-only per-container mount.
set -eu
# Refuse to relabel an older runtime as Android14.
[ "$(getprop ro.build.version.release)" = "14" ]
[ "$(getprop ro.build.version.sdk)" = "34" ]
/system/bin/magisk resetprop -n -f /simufarm/identity.prop
setprop sys.simufarm.identity.ready 1
