#include <pcap.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) {
        return 0;
    }

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;
    struct bpf_program fp;
    struct pcap_pkthdr *header;
    const u_char *packet;

    int snaplen = (data[0] << 8) | data[1];
    int timeout = (data[2] << 8) | data[3];
    int filter_len = (data[4] << 8) | data[5];
    
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

    if (size > 6 + filter_len) {
        char filter_exp[256];
        size_t copy_len = (filter_len > 255) ? 255 : filter_len;
        memcpy(filter_exp, data + 6, copy_len);
        filter_exp[copy_len] = '\0';

        if (pcap_compile(handle, &fp, filter_exp, 0, PCAP_NETMASK_UNKNOWN) == 0) {
            pcap_setfilter(handle, &fp);
            pcap_freecode(&fp);
        }
    }

    int iterations = 0;
    while (iterations < 10) {
        int res = pcap_next_ex(handle, &header, &packet);
        if (res <= 0) break;
        
        if (header->len >= 42) {
            uint8_t proto = packet[23];
            if (proto == 17) {
                // UDP traffic detected
            }
        }
        iterations++;
    }

    pcap_close(handle);
    return 0;
}