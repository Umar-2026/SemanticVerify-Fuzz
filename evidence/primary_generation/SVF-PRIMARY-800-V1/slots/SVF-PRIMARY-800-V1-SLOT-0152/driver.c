#include <pcap.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 64) {
        return 0;
    }

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_create("lo", errbuf);
    if (!handle) {
        return 0;
    }

    pcap_set_snaplen(handle, 65535);
    pcap_set_promisc(handle, 1);
    pcap_set_timeout(handle, 1);

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    struct bpf_program fp;
    const char *filter_exp = "udp";
    if (pcap_compile(handle, &fp, filter_exp, 0, PCAP_NETMASK_UNKNOWN) == 0) {
        if (pcap_setfilter(handle, &fp) == 0) {
            struct pcap_pkthdr *header;
            const u_char *pkt_data;
            
            int status = pcap_next_ex(handle, &header, &pkt_data);
            if (status == 1) {
                if (header->len >= 42) {
                    uint16_t *eth_type = (uint16_t *)(pkt_data + 12);
                    if (*eth_type == 0x0008) {
                        uint8_t *proto = (uint8_t *)(pkt_data + 23);
                        if (*proto == 17) {
                            volatile uint8_t check = pkt_data[41];
                            (void)check;
                        }
                    }
                }
            }
        }
        pcap_freecode(&fp);
    }

    pcap_close(handle);
    return 0;
}