#include <pcap.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) {
        return 0;
    }

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;
    struct bpf_program fp;
    struct pcap_pkthdr *header;
    const u_char *packet;

    int snaplen = (data[0] << 8) | data[1];
    int timeout = (data[2] << 8) | data[3];
    
    handle = pcap_create("lo", errbuf);
    if (!handle) {
        return 0;
    }

    pcap_set_snaplen(handle, snaplen > 0 ? snaplen : 65535);
    pcap_set_timeout(handle, timeout);
    pcap_set_promisc(handle, 1);

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    if (pcap_compile(handle, &fp, "udp", 0, PCAP_NETMASK_UNKNOWN) == 0) {
        pcap_setfilter(handle, &fp);
        pcap_freecode(&fp);
    }

    int iterations = data[4] % 10;
    for (int i = 0; i < iterations; i++) {
        int res = pcap_next_ex(handle, &header, &packet);
        if (res == 1) {
            if (header->len > 0 && header->len <= header->caplen) {
                volatile uint8_t byte = packet[0];
                (void)byte;
            }
        } else if (res < 0) {
            break;
        }
    }

    pcap_close(handle);
    return 0;
}