#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/udp.h>
#include <netinet/ip.h>
#include <unistd.h>
#include <errno.h>

#define MAX_DATAGRAMS 16
#define MAX_PACKET_SIZE 65535

static int send_udp_datagram(const uint8_t *data, size_t len) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) return -1;

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(9999);

    ssize_t sent = sendto(fd, data, len, 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
    return (sent == (ssize_t)len) ? 0 : -1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    uint8_t num_datagrams = data[0] % MAX_DATAGRAMS;
    if (num_datagrams == 0) return 0;

    size_t offset = 1;
    size_t per_datagram_size = (size - 1) / num_datagrams;
    if (per_datagram_size == 0) return 0;

    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    if (pcap_set_snaplen(handle, MAX_PACKET_SIZE) != 0) {
        pcap_close(handle);
        return 0;
    }
    if (pcap_set_promisc(handle, 0) != 0) {
        pcap_close(handle);
        return 0;
    }
    if (pcap_set_timeout(handle, 100) != 0) {
        pcap_close(handle);
        return 0;
    }

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    for (uint8_t i = 0; i < num_datagrams; i++) {
        size_t start = offset + i * per_datagram_size;
        size_t len = per_datagram_size;
        if (start + len > size) len = size - start;
        if (len == 0) break;

        if (send_udp_datagram(data + start, len) != 0) {
            pcap_close(handle);
            return 0;
        }
    }

    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int packets_seen = 0;
    int result;

    while (packets_seen < num_datagrams) {
        result = pcap_next_ex(handle, &header, &packet_data);
        if (result == 1) {
            packets_seen++;
        } else if (result == 0) {
            continue;
        } else {
            break;
        }
    }

    pcap_close(handle);
    return 0;
}