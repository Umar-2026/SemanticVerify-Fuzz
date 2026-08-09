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

    if (pcap_set_timeout(handle, 10) != 0) {
        pcap_close(handle);
        return 0;
    }

    int status = pcap_activate(handle);
    if (status != 0) {
        pcap_close(handle);
        return 0;
    }

    int iterations = data[0] % 5;
    for (int i = 0; i < iterations; i++) {
        int res = pcap_next_ex(handle, &header, &pkt_data);
        if (res == 1) {
            // Packet captured successfully
        } else if (res == 0) {
            // Timeout reached
        } else if (res < 0) {
            // Error or EOF
            break;
        }
    }

    pcap_close(handle);
    return 0;
}