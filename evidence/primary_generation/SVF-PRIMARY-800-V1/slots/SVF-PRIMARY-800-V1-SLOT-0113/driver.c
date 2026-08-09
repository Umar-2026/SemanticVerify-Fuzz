#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    uint32_t snaplen = (uint32_t)data[0] | ((uint32_t)data[1] << 8) | ((uint32_t)data[2] << 16) | ((uint32_t)data[3] << 24);
    uint32_t timeout = (uint32_t)data[4] | ((uint32_t)data[5] << 8) | ((uint32_t)data[6] << 16) | ((uint32_t)data[7] << 24);

    /* Bound the values to reasonable ranges */
    if (snaplen > 65535) snaplen = 65535;
    if (timeout > 10000) timeout = 10000;

    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    if (pcap_set_snaplen(handle, (int)snaplen) != 0) {
        pcap_close(handle);
        return 0;
    }
    if (pcap_set_timeout(handle, (int)timeout) != 0) {
        pcap_close(handle);
        return 0;
    }
    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    struct pcap_pkthdr *header;
    const u_char *packet;
    int ret = pcap_next_ex(handle, &header, &packet);
    if (ret == 1) {
        /* Inspect the packet: just check it's non-null and header is valid */
        if (packet != NULL && header != NULL) {
            /* Do nothing with the data, just ensure it's accessible */
            volatile uint8_t sum = 0;
            size_t len = header->caplen;
            if (len > 0 && packet != NULL) {
                for (size_t i = 0; i < len; i++) {
                    sum += packet[i];
                }
            }
            (void)sum;
        }
    }

    pcap_close(handle);
    return 0;
}