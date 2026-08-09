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
    int filter_len = data[4] % 64;

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

    if (size > 5 + filter_len) {
        char filter_exp[65];
        memcpy(filter_exp, &data[5], filter_len);
        filter_exp[filter_len] = '\0';

        if (pcap_compile(handle, &fp, filter_exp, 0, PCAP_NETMASK_UNKNOWN) == 0) {
            pcap_setfilter(handle, &fp);
            pcap_freecode(&fp);
        }
    }

    int count = 0;
    while (count < 10 && pcap_next_ex(handle, &header, &packet) == 1) {
        if (header->len >= 42) {
            uint8_t proto = packet[23];
            if (proto == 17) {
                uint16_t dst_port = (packet[40] << 8) | packet[41];
                (void)dst_port;
            }
        }
        count++;
    }

    pcap_close(handle);
    return 0;
}