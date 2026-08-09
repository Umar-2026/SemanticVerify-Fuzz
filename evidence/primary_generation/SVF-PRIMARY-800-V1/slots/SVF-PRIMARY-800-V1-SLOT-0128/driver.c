#include <pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;

    handle = pcap_create("lo", errbuf);
    if (handle == NULL) {
        return 0;
    }

    if (pcap_set_snaplen(handle, (int)(data[0] % 65535)) != 0) {
        pcap_close(handle);
        return 0;
    }

    if (pcap_set_timeout(handle, 100) != 0) {
        pcap_close(handle);
        return 0;
    }

    if (pcap_activate(handle) == 0) {
        int dlt = pcap_datalink(handle);
        (void)dlt;
    }

    pcap_close(handle);
    return 0;
}