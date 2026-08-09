#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#include <errno.h>

#define MAX_SNAPLEN 65535
#define MAX_TIMEOUT 1000

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    uint16_t snaplen = (uint16_t)((data[0] << 8) | data[1]);
    uint16_t timeout = (uint16_t)((data[2] << 8) | data[3]);
    if (snaplen > MAX_SNAPLEN) snaplen = MAX_SNAPLEN;
    if (timeout > MAX_TIMEOUT) timeout = MAX_TIMEOUT;

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *p = pcap_create("lo", errbuf);
    if (p == NULL) return 0;

    if (pcap_set_snaplen(p, snaplen) != 0) {
        pcap_close(p);
        return 0;
    }
    if (pcap_set_timeout(p, timeout) != 0) {
        pcap_close(p);
        return 0;
    }
    if (pcap_activate(p) != 0) {
        pcap_close(p);
        return 0;
    }

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        pcap_close(p);
        return 0;
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(0);

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(sock);
        pcap_close(p);
        return 0;
    }

    socklen_t len = sizeof(addr);
    if (getsockname(sock, (struct sockaddr *)&addr, &len) < 0) {
        close(sock);
        pcap_close(p);
        return 0;
    }

    char payload[4] = {0xde, 0xad, 0xbe, 0xef};
    if (sendto(sock, payload, sizeof(payload), 0, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(sock);
        pcap_close(p);
        return 0;
    }

    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int ret = pcap_next_ex(p, &header, &packet_data);
    if (ret == 1) {
        // Consume the packet data (bounded by snaplen)
        volatile uint32_t sum = 0;
        for (uint32_t i = 0; i < header->caplen && i < snaplen; i++) {
            sum += packet_data[i];
        }
        (void)sum;
    }

    close(sock);
    pcap_close(p);
    return 0;
}