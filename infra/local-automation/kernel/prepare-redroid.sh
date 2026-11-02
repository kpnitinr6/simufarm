#!/bin/sh
set -eu
modprobe binder_linux devices=binder,hwbinder,vndbinder
modprobe ashmem_linux
mkdir -p /dev/binderfs
if ! mountpoint -q /dev/binderfs; then
    mount -t binder binder /dev/binderfs
fi
