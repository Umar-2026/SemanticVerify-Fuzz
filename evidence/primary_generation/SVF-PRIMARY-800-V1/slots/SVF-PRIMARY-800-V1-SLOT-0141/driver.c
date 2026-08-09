#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_create("lo", errbuf);
    if (handle == NULL) {
        return 0;
    }

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    int datalink = pcap_datalink(handle);

    struct pcap_pkthdr *header;
    const u_char *packet_data;

    int result = pcap_next_ex(handle, &header, &packet_data);
    if (result == 1) {
        if (header->caplen > 0 && packet_data != NULL) {
            volatile uint8_t sum = 0;
            size_t inspect_len = header->caplen;
            if (inspect_len > size) {
                inspect_len = size;
            }
            for (size_t i = 0; i < inspect_len; i++) {
                sum += packet_data[i];
            }
            (void)sum;
        }
    } else if (result == 0) {
        /* timeout, no packet */
    } else {
        /* error or break */
    }

    pcap_close(handle);
    return 0;
}