#include <pcap/pcap.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <net/if.h>
#include <errno.h>

#define BUF_SIZE 65536

static int send_udp_packet(void) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) return -1;

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(9999);

    const char *payload = "hello";
    int ret = sendto(fd, payload, strlen(payload), 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
    return ret;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *p = pcap_create("lo", errbuf);
    if (p == NULL) return 0;

    pcap_set_snaplen(p, 65535);
    pcap_set_promisc(p, 0);
    pcap_set_timeout(p, 100);

    if (pcap_activate(p) != 0) {
        pcap_close(p);
        return 0;
    }

    struct bpf_program fp;
    char filter_expr[128];
    size_t filter_len = size < sizeof(filter_expr) ? size : sizeof(filter_expr) - 1;
    memcpy(filter_expr, data, filter_len);
    filter_expr[filter_len] = '\0';

    if (pcap_compile(p, &fp, filter_expr, 1, PCAP_NETMASK_UNKNOWN) != 0) {
        pcap_close(p);
        return 0;
    }

    if (pcap_setfilter(p, &fp) != 0) {
        pcap_freecode(&fp);
        pcap_close(p);
        return 0;
    }

    pcap_freecode(&fp);

    if (send_udp_packet() < 0) {
        pcap_close(p);
        return 0;
    }

    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int ret = pcap_next_ex(p, &header, &packet_data);
    if (ret == 1) {
        if (header->caplen > 0) {
            volatile uint8_t sum = 0;
            for (uint32_t i = 0; i < header->caplen && i < 64; i++) {
                sum += packet_data[i];
            }
            (void)sum;
        }
    }

    pcap_close(p);
    return 0;
}