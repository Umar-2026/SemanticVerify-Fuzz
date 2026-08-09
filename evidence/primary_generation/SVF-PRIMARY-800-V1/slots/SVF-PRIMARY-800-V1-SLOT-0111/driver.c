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
    snaplen = snaplen % (MAX_SNAPLEN + 1);
    timeout = timeout % (MAX_TIMEOUT + 1);

    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    if (pcap_set_snaplen(handle, snaplen) != 0) {
        pcap_close(handle);
        return 0;
    }
    if (pcap_set_timeout(handle, timeout) != 0) {
        pcap_close(handle);
        return 0;
    }
    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        pcap_close(handle);
        return 0;
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(9999);

    char payload[4] = {0xde, 0xad, 0xbe, 0xef};
    if (sendto(sock, payload, sizeof(payload), 0, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(sock);
        pcap_close(handle);
        return 0;
    }

    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int ret = pcap_next_ex(handle, &header, &packet_data);
    if (ret == 1) {
        // Packet received, do nothing with it
    }

    close(sock);
    pcap_close(handle);
    return 0;
}