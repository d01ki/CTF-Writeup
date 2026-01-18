#!/bin/bash

cd /home/pwn/
exec timeout --foreground 180 /home/pwn/qemu-system-x86_64 \
	-nographic \
        -kernel bzImage \
        -initrd initramfs.cpio.gz \
        -device ASISD \
        -m 256M \
	-L ./pc-bios/ \
        -no-reboot \
        -monitor none \
        -sandbox on,obsolete=deny,elevateprivileges=deny,resourcecontrol=deny \
        -append "console=ttyS0 oops=panic panic=1 quiet"
       

