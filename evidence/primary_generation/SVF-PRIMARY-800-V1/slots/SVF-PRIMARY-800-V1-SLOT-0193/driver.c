#include <pcap/pcap.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#include <errno.h>

#define MAX_PACKETS 64
#define MAX_FILTER_LEN 256

static int send_udp_packet(uint16_t src_port, uint16_t dst_port, const uint8_t *payload, size_t payload_len) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) return -1;

    struct sockaddr_in src_addr;
    memset(&src_addr, 0, sizeof(src_addr));
    src_addr.sin_family = AF_INET;
    src_addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    src_addr.sin_port = htons(src_port);
    if (bind(fd, (struct sockaddr *)&src_addr, sizeof(src_addr)) < 0) {
        close(fd);
        return -1;
    }

    struct sockaddr_in dst_addr;
    memset(&dst_addr, 0, sizeof(dst_addr));
    dst_addr.sin_family = AF_INET;
    dst_addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    dst_addr.sin_port = htons(dst_port);

    ssize_t sent = sendto(fd, payload, payload_len, 0, (struct sockaddr *)&dst_addr, sizeof(dst_addr));
    close(fd);
    return (sent == (ssize_t)payload_len) ? 0 : -1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Parse input: [2 bytes snaplen][2 bytes timeout][2 bytes src_port][2 bytes dst_port][rest: filter string]
    uint16_t snaplen = (uint16_t)(data[0] | (data[1] << 8));
    uint16_t timeout_ms = (uint16_t)(data[2] | (data[3] << 8));
    uint16_t src_port = (uint16_t)(data[4] | (data[5] << 8));
    uint16_t dst_port = (uint16_t)(data[6] | (data[7] << 8));

    // Clamp snaplen to reasonable bounds
    if (snaplen < 64) snaplen = 64;
    if (snaplen > 65535) snaplen = 65535;

    // Build filter string from remaining bytes, bounded
    char filter[MAX_FILTER_LEN];
    size_t filter_len = size - 8;
    if (filter_len >= MAX_FILTER_LEN) filter_len = MAX_FILTER_LEN - 1;
    memcpy(filter, data + 8, filter_len);
    filter[filter_len] = '\0';

    // Create and configure capture handle
    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    pcap_set_snaplen(handle, snaplen);
    pcap_set_timeout(handle, timeout_ms);
    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    // Compile and set filter
    struct bpf_program fp;
    if (pcap_compile(handle, &fp, filter, 1, PCAP_NETMASK_UNKNOWN) == 0) {
        if (pcap_setfilter(handle, &fp) == 0) {
            // Send a UDP packet to loopback to generate traffic
            uint8_t payload[16] = {0xde, 0xad, 0xbe, 0xef, 0x01, 0x02, 0x03, 0x04,
                                   0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c};
            send_udp_packet(src_port, dst_port, payload, sizeof(payload));

            // Capture a bounded number of packets
            struct pcap_pkthdr *header;
            const u_char *packet_data;
            int packets_seen = 0;
            while (packets_seen < MAX_PACKETS) {
                int result = pcap_next_ex(handle, &header, &packet_data);
                if (result == 1) {
                    // Inspect packet: just count and optionally check length
                    if (header->len > 0 && packet_data != NULL) {
                        packets_seen++;
                    }
                } else if (result == 0) {
                    // Timeout expired
                    break;
                } else {
                    // Error or EOF
                    break;
                }
            }
        }
        pcap_freecode(&fp);
    }

    pcap_close(handle);
    return 0;
}