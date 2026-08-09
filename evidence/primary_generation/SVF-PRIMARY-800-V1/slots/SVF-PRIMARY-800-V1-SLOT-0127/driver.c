#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = NULL;

    /* Use input to derive a snapshot length (bounded to a reasonable range). */
    uint32_t snap_raw = 0;
    memcpy(&snap_raw, data, 4);
    int snap = (int)(snap_raw % 65536) + 1; /* 1..65536 */

    /* Use input to derive a promiscuous flag. */
    int promisc = (size > 4) ? (data[4] & 1) : 0;

    /* Use input to derive a timeout (bounded). */
    int timeout = 0;
    if (size > 5) {
        timeout = (int)(data[5] % 1000);
    }

    handle = pcap_create("lo", errbuf);
    if (handle == NULL) {
        return 0;
    }

    pcap_set_snaplen(handle, snap);
    pcap_set_promisc(handle, promisc);
    pcap_set_timeout(handle, timeout);

    int status = pcap_activate(handle);
    if (status != 0) {
        pcap_close(handle);
        return 0;
    }

    /* Report a capture property when an active context is available. */
    int linktype = pcap_datalink(handle);
    if (linktype >= 0) {
        /* Consume the value to avoid unused warnings; no external output. */
        volatile int sink = linktype;
        (void)sink;
    }

    pcap_close(handle);
    return 0;
}