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
    if (size < 4) return 0;

    /* Parse number of datagrams (bounded) and per-datagram sizes from fuzz input */
    uint32_t count_raw;
    memcpy(&count_raw, data, 4);
    size_t count = count_raw % MAX_DATAGRAMS;
    size_t offset = 4;

    /* Build a simple size table from the remaining bytes */
    size_t sizes[MAX_DATAGRAMS];
    size_t total_payload = 0;
    for (size_t i = 0; i < count; i++) {
        if (offset >= size) {
            sizes[i] = 0;
        } else {
            sizes[i] = data[offset] % 256;
            offset++;
        }
        total_payload += sizes[i];
        if (total_payload > size - offset) {
            /* Not enough payload bytes; truncate remaining sizes */
            for (size_t j = i; j < count; j++) sizes[j] = 0;
            break;
        }
    }

    /* Create and activate loopback capture */
    pcap_t *pcap = pcap_create("lo", NULL);
    if (pcap == NULL) return 0;

    if (pcap_set_snaplen(pcap, MAX_PACKET_SIZE) != 0) {
        pcap_close(pcap);
        return 0;
    }
    if (pcap_set_promisc(pcap, 0) != 0) {
        pcap_close(pcap);
        return 0;
    }
    if (pcap_set_timeout(pcap, 100) != 0) {
        pcap_close(pcap);
        return 0;
    }
    if (pcap_activate(pcap) != 0) {
        pcap_close(pcap);
        return 0;
    }

    /* Emit datagrams derived from fuzz payload */
    size_t payload_offset = offset;
    for (size_t i = 0; i < count; i++) {
        size_t dlen = sizes[i];
        if (dlen == 0) continue;
        if (payload_offset + dlen > size) break;
        send_udp_datagram(data + payload_offset, dlen);
        payload_offset += dlen;
    }

    /* Capture a bounded number of packets */
    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int packets_seen = 0;
    int max_packets = (int)(count * 2 + 1);
    if (max_packets > 64) max_packets = 64;

    for (int i = 0; i < max_packets; i++) {
        int rc = pcap_next_ex(pcap, &header, &packet_data);
        if (rc == 1) {
            packets_seen++;
            /* Consume packet data to prevent optimization */
            volatile uint32_t sum = 0;
            for (uint32_t j = 0; j < header->caplen && j < 64; j++) {
                sum += packet_data[j];
            }
            (void)sum;
        } else if (rc == 0) {
            /* Timeout */
            break;
        } else {
            /* Error or EOF */
            break;
        }
    }

    pcap_close(pcap);
    return 0;
}