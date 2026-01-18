import pyshark
import os

cap = pyshark.FileCapture(
    "usbstorage.pcapng", display_filter="scsi", include_raw=True, use_json=True
)
last = None
addr = 0
mapping = dict()
for pkt in cap:
    if "scsi" in pkt:
        s = str(pkt)
        if "scsi_sbc.opcode" in pkt.scsi.field_names:
            if pkt.scsi.get("scsi_sbc.opcode") == "0x2a":
                if "scsi_sbc.rdwr10.lba" in pkt.scsi.field_names:
                    print("LBA", pkt.scsi.get("scsi_sbc.rdwr10.lba"))
                    addr = int(pkt.scsi.get("scsi_sbc.rdwr10.lba"), 16) * 512
                else:
                    data = pkt.get_raw_packet()[0x40:]
                    if len(data) % 512 != 0:
                        continue
                    print(f"Write 0x{len(data):x} bytes to 0x{addr:x} (LBA 0x{addr//512:x})")
                    for i in range(0, len(data), 512):
                        mapping[addr + i] = data[i:i+512]

for key in list(sorted(mapping.keys())):
    addr = key
    if addr not in mapping:
        continue
    disk = open(f"usbstorage{addr//512:x}.img", "wb")
    while addr in mapping:
        data = mapping[addr]
        disk.write(data)
        del mapping[addr]
        addr += len(data)