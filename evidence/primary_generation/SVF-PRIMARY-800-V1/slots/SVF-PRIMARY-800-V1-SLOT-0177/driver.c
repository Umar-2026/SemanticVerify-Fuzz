#include <pcap/pcap.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <net/if.h>

#define BUF_SIZE 65536

static void emit_udp_packet(void) {
    int s = socket(AF_INET, SOCK_DGRAM, 0);
    if (s < 0) return;
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(9999);
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    const char *payload = "hello";
    sendto(s, payload, strlen(payload), 0, (struct sockaddr *)&addr, sizeof(addr));
    close(s);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

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

    // Build a filter program from fuzz data (bounded)
    char filter[128];
    size_t flen = size < sizeof(filter) - 1 ? size : sizeof(filter) - 1;
    memcpy(filter, data, flen);
    filter[flen] = '\0';

    struct bpf_program fp;
    if (pcap_compile(p, &fp, filter, 1, PCAP_NETMASK_UNKNOWN) != 0) {
        pcap_close(p);
        return 0;
    }

    if (pcap_setfilter(p, &fp) != 0) {
        pcap_freecode(&fp);
        pcap_close(p);
        return 0;
    }
    pcap_freecode(&fp);

    // Emit a local UDP packet to trigger capture
    emit_udp_packet();

    // Capture a bounded number of packets
    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int count = 0;
    while (count < 10) {
        int ret = pcap_next_ex(p, &header, &packet_data);
        if (ret == 1) {
            // Process packet data (bounded)
            if (header->caplen > 0) {
                volatile uint8_t sum = 0;
                size_t n = header->caplen < 64 ? header->caplen : 64;
                for (size_t i = 0; i < n; i++) {
                    sum += packet_data[i];
                }
                (void)sum;
            }
            count++;
        } else if (ret == 0) {
            // Timeout, try again
            continue;
        } else {
            // Error or break
            break;
        }
    }

    pcap_close(p);
    return 0;
}