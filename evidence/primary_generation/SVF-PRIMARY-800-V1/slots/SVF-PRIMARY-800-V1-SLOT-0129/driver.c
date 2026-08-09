#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    // Use input to derive a snapshot length (bounded to a reasonable range)
    uint32_t snap_len = 0;
    memcpy(&snap_len, data, sizeof(snap_len));
    snap_len = snap_len % 65536 + 1; // 1..65536

    // Use input to derive a promiscuous flag
    int promisc = (data[4] & 1) ? 1 : 0;

    // Use input to derive a timeout (bounded)
    uint32_t timeout_ms = 0;
    if (size >= 8) {
        memcpy(&timeout_ms, data + 4, sizeof(timeout_ms));
    }
    timeout_ms = timeout_ms % 10000; // 0..9999 ms

    // Create a loopback capture handle
    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) {
        return 0;
    }

    // Set options from input
    pcap_set_snaplen(handle, (int)snap_len);
    pcap_set_promisc(handle, promisc);
    pcap_set_timeout(handle, (int)timeout_ms);

    // Attempt activation
    int status = pcap_activate(handle);
    if (status != 0) {
        pcap_close(handle);
        return 0;
    }

    // Report a capture property when active
    int datalink = pcap_datalink(handle);
    if (datalink < 0) {
        pcap_close(handle);
        return 0;
    }

    // Use the datalink value in a way that prevents optimization
    volatile int sink = datalink;
    (void)sink;

    pcap_close(handle);
    return 0;
}