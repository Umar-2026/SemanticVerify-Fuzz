#include <pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) {
        return 0;
    }

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;
    struct pcap_pkthdr *header;
    const u_char *pkt_data;

    int snaplen = (data[0] << 8) | data[1];
    int timeout = (data[2] << 8) | data[3];

    handle = pcap_create("lo", errbuf);
    if (handle == NULL) {
        return 0;
    }

    if (pcap_set_snaplen(handle, snaplen) != 0) {
        pcap_close(handle);
        return 0;
    }

    if (pcap_set_timeout(handle, timeout) != 0) {
        pcap_close(handle);
        return 0;
    }

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    int status = pcap_next_ex(handle, &header, &pkt_data);
    if (status == 1) {
        // Successfully captured a packet, inspect header/data if needed
        (void)header;
        (void)pkt_data;
    }

    pcap_close(handle);
    return 0;
}