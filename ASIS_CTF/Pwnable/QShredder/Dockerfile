FROM ubuntu:25.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
xinetd libpixman-1-dev libepoxy-dev libspice-server-dev libfdt-dev \
libusb-1.0.0-dev libasound-dev libaio-dev libslirp-dev libgtk-3-0 \
libbrlapi-dev libcurl4-openssl-dev 

RUN apt-get clean
RUN useradd -m pwn

COPY flag /home/pwn/flag
COPY qemu-system-x86_64 /home/pwn/qemu-system-x86_64
COPY pc-bios /home/pwn/pc-bios
COPY run.sh /home/pwn/run.sh
COPY bzImage /home/pwn/bzImage
COPY initramfs.cpio.gz /home/pwn/initramfs.cpio.gz
COPY xinetd /etc/xinetd.d/shreder

RUN chown -R pwn:pwn /home/pwn/

USER pwn
WORKDIR /home/pwn
EXPOSE 11337
CMD ["/usr/sbin/xinetd", "-dontfork"]
