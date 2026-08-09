#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
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
    addr.sin_port = htons(9); /* discard port */

    ssize_t sent = sendto(fd, data, len, 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
    return (sent == (ssize_t)len) ? 0 : -1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    /* Parse number of datagrams (1..MAX_DATAGRAMS) from first byte */
    size_t num_datagrams = (data[0] % MAX_DATAGRAMS) + 1;
    size_t offset = 1;

    /* Create and activate loopback capture */
    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    /* Send datagrams derived from fuzz input */
    for (size_t i = 0; i < num_datagrams && offset < size; i++) {
        size_t remaining = size - offset;
        size_t dgram_len = remaining;
        if (dgram_len > MAX_PACKET_SIZE) dgram_len = MAX_PACKET_SIZE;

        /* Ensure at least 1 byte per datagram */
        if (dgram_len == 0) break;

        send_udp_datagram(data + offset, dgram_len);
        offset += dgram_len;
    }

    /* Capture and process packets for a bounded time */
    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int packets_seen = 0;
    int max_packets = (int)(num_datagrams * 2); /* allow some overhead */

    while (packets_seen < max_packets) {
        int ret = pcap_next_ex(handle, &header, &packet_data);
        if (ret == 1) {
            /* Process packet: just validate header fields */
            if (header->caplen > 0 && packet_data != NULL) {
                packets_seen++;
            }
        } else if (ret == 0) {
            /* Timeout: continue */
            continue;
        } else {
            /* Error or EOF: stop */
            break;
        }
    }

    pcap_close(handle);
    return 0;
}