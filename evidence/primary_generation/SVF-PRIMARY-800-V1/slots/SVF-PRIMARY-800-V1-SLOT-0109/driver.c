#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    pcap_t *pcap = pcap_create("lo", NULL);
    if (pcap == NULL) return 0;

    pcap_set_promisc(pcap, 0);
    pcap_set_snaplen(pcap, 65535);
    pcap_set_timeout(pcap, 100);

    if (pcap_activate(pcap) != 0) {
        pcap_close(pcap);
        return 0;
    }

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        pcap_close(pcap);
        return 0;
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(0);

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(sock);
        pcap_close(pcap);
        return 0;
    }

    socklen_t addrlen = sizeof(addr);
    if (getsockname(sock, (struct sockaddr *)&addr, &addrlen) < 0) {
        close(sock);
        pcap_close(pcap);
        return 0;
    }

    size_t payload_len = size < 2 ? 0 : size - 2;
    if (payload_len > 1400) payload_len = 1400;

    if (sendto(sock, data + 2, payload_len, 0, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(sock);
        pcap_close(pcap);
        return 0;
    }

    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int ret = pcap_next_ex(pcap, &header, &packet_data);
    if (ret == 1) {
        volatile uint32_t sum = 0;
        for (uint32_t i = 0; i < header->caplen && i < 64; i++) {
            sum += packet_data[i];
        }
        (void)sum;
    }

    close(sock);
    pcap_close(pcap);
    return 0;
}