#include <pcap.h>
#include <stdlib.h>
#include <stdint.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;
    struct pcap_pkthdr *header;
    const u_char *pkt_data;

    handle = pcap_create("lo", errbuf);
    if (handle == NULL) {
        return 0;
    }

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    int dlt = pcap_datalink(handle);
    (void)dlt;

    int status = pcap_next_ex(handle, &header, &pkt_data);
    if (status == 1) {
        if (header->caplen > 0 && pkt_data != NULL) {
            volatile uint8_t sink = pkt_data[0];
            (void)sink;
        }
    }

    pcap_close(handle);
    return 0;
}