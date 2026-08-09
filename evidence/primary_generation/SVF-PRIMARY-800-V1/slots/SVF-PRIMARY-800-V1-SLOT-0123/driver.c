#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    // Use first 4 bytes to derive a bounded snaplen (1 to 65535)
    uint32_t snaplen_raw = 0;
    memcpy(&snaplen_raw, data, 4);
    int snaplen = (int)(snaplen_raw % 65535) + 1;

    // Use next 4 bytes to derive a bounded timeout (0 to 1000 ms)
    uint32_t timeout_raw = 0;
    if (size >= 8) {
        memcpy(&timeout_raw, data + 4, 4);
    }
    int timeout_ms = (int)(timeout_raw % 1001);

    // Use next 2 bytes to derive a bounded buffer size (1 to 65535)
    uint32_t bufsize_raw = 0;
    if (size >= 10) {
        memcpy(&bufsize_raw, data + 8, 2);
    }
    int bufsize = (int)(bufsize_raw % 65535) + 1;

    // Use next byte to derive a bounded promiscuous flag (0 or 1)
    int promisc = 0;
    if (size >= 11) {
        promisc = (data[10] & 1);
    }

    // Use next byte to derive a bounded immediate mode flag (0 or 1)
    int immediate = 0;
    if (size >= 12) {
        immediate = (data[11] & 1);
    }

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_create("lo", errbuf);
    if (handle == NULL) {
        return 0;
    }

    pcap_set_snaplen(handle, snaplen);
    pcap_set_timeout(handle, timeout_ms);
    pcap_set_buffer_size(handle, bufsize);
    pcap_set_promisc(handle, promisc);
    pcap_set_immediate_mode(handle, immediate);

    int status = pcap_activate(handle);
    if (status == 0) {
        int linktype = pcap_datalink(handle);
        // Report a capture property when active context is available
        if (linktype >= 0) {
            // Consume the property to avoid unused warning
            volatile int report = linktype;
            (void)report;
        }
    }

    pcap_close(handle);
    return 0;
}