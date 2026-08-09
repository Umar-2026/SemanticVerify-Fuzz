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
    (void)datalink;

    struct pcap_pkthdr *header;
    const u_char *packet_data;

    int result = pcap_next_ex(handle, &header, &packet_data);
    if (result == 1) {
        if (header->caplen > 0 && packet_data != NULL) {
            size_t copy_len = header->caplen;
            if (copy_len > size) {
                copy_len = size;
            }
            volatile uint8_t sum = 0;
            for (size_t i = 0; i < copy_len; i++) {
                sum += packet_data[i];
            }
            (void)sum;
        }
    }

    pcap_close(handle);
    return 0;
}