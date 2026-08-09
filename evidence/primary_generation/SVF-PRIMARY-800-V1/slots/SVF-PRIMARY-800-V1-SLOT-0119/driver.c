#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>

#define FUZZ_MAX_SNAPLEN 65535
#define FUZZ_MAX_TIMEOUT 1000

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    uint16_t snaplen = (uint16_t)(data[0] | (data[1] << 8));
    uint16_t timeout = (uint16_t)(data[2] | (data[3] << 8));
    uint16_t port = (uint16_t)(data[4] | (data[5] << 8));
    uint16_t payload_len = (uint16_t)(data[6] | (data[7] << 8));

    if (snaplen > FUZZ_MAX_SNAPLEN) snaplen = FUZZ_MAX_SNAPLEN;
    if (timeout > FUZZ_MAX_TIMEOUT) timeout = FUZZ_MAX_TIMEOUT;
    if (payload_len > 1400) payload_len = 1400;

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *pcap = pcap_create("lo", errbuf);
    if (pcap == NULL) return 0;

    if (pcap_set_snaplen(pcap, snaplen) != 0) {
        pcap_close(pcap);
        return 0;
    }
    if (pcap_set_timeout(pcap, timeout) != 0) {
        pcap_close(pcap);
        return 0;
    }
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
    addr.sin_port = htons(port);

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(sock);
        pcap_close(pcap);
        return 0;
    }

    uint8_t *payload = (uint8_t *)malloc(payload_len ? payload_len : 1);
    if (payload == NULL) {
        close(sock);
        pcap_close(pcap);
        return 0;
    }
    if (payload_len > 0) {
        memcpy(payload, data + 8, payload_len > (size - 8) ? (size - 8) : payload_len);
    }

    ssize_t sent = sendto(sock, payload, payload_len, 0, (struct sockaddr *)&addr, sizeof(addr));
    free(payload);
    if (sent < 0) {
        close(sock);
        pcap_close(pcap);
        return 0;
    }

    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int result = pcap_next_ex(pcap, &header, &packet_data);
    if (result == 1) {
        // Packet captured; no further processing needed.
    }

    close(sock);
    pcap_close(pcap);
    return 0;
}