#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    // Use first byte for snaplen (bounded to 1..65535)
    uint32_t snaplen = (uint32_t)data[0] + 1;
    if (snaplen > 65535) {
        snaplen = 65535;
    }

    // Use second byte for promiscuous flag (0 or 1)
    int promisc = data[1] & 1;

    // Use third byte for timeout (bounded to 0..1000 ms)
    int timeout_ms = data[2] % 1001;

    // Use fourth byte for buffer size (bounded to 0..1000000)
    int buffer_size = (int)(data[3] * 10000);
    if (buffer_size > 1000000) {
        buffer_size = 1000000;
    }

    // Remaining bytes are used as a device name (null-terminated, bounded)
    char devname[256];
    size_t devlen = size - 4;
    if (devlen > sizeof(devname) - 1) {
        devlen = sizeof(devname) - 1;
    }
    memcpy(devname, data + 4, devlen);
    devname[devlen] = '\0';

    pcap_t *handle = pcap_create(devname, NULL);
    if (handle == NULL) {
        return 0;
    }

    pcap_set_snaplen(handle, snaplen);
    pcap_set_promisc(handle, promisc);
    pcap_set_timeout(handle, timeout_ms);
    pcap_set_buffer_size(handle, buffer_size);

    int status = pcap_activate(handle);
    if (status == 0) {
        int linktype = pcap_datalink(handle);
        // Report the datalink type as an integer (no output, just exercise the API)
        (void)linktype;
    }

    pcap_close(handle);
    return 0;
}