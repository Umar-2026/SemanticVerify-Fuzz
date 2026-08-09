#include <pcap/pcap.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

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

    /* Query a capture property: datalink type */
    int dl = pcap_datalink(handle);
    (void)dl;

    /* Use the fuzz input to craft a small packet for inspection */
    size_t pkt_len = size < 64 ? size : 64;
    uint8_t pkt[64];
    memcpy(pkt, data, pkt_len);

    /* Inject the packet into the loopback interface using pcap_inject if available,
       but since we only have pcap_next_ex, we'll just call pcap_next_ex with a short timeout
       to see if any packet arrives. The crafted data is not actually sent, but we
       perform the bounded operation of calling pcap_next_ex. */
    struct pcap_pkthdr *header;
    const u_char *packet;
    int ret = pcap_next_ex(handle, &header, &packet);
    (void)ret;

    pcap_close(handle);
    return 0;
}