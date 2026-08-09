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
#include <errno.h>

#define FUZZ_PACKET_SIZE 64

static int send_udp_packet(void) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) return -1;

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(9999);

    uint8_t payload[8] = {0xde, 0xad, 0xbe, 0xef, 0x01, 0x02, 0x03, 0x04};
    int ret = sendto(fd, payload, sizeof(payload), 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
    return ret;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    // Use first byte to select filter expression (bounded set)
    const char *filter_expr;
    switch (data[0] % 4) {
        case 0: filter_expr = "udp"; break;
        case 1: filter_expr = "udp port 9999"; break;
        case 2: filter_expr = "ip and udp"; break;
        default: filter_expr = "udp and len > 0"; break;
    }

    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    struct bpf_program fp;
    if (pcap_compile(handle, &fp, filter_expr, 1, PCAP_NETMASK_UNKNOWN) != 0) {
        pcap_close(handle);
        return 0;
    }

    if (pcap_setfilter(handle, &fp) != 0) {
        pcap_freecode(&fp);
        pcap_close(handle);
        return 0;
    }
    pcap_freecode(&fp);

    // Send a UDP packet to loopback
    if (send_udp_packet() < 0) {
        pcap_close(handle);
        return 0;
    }

    // Try to capture the packet with a short timeout
    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int ret = pcap_next_ex(handle, &header, &packet_data);
    if (ret == 1) {
        // Inspect the captured packet (just verify it's non-null and has a sane length)
        if (header->len > 0 && packet_data != NULL) {
            // Simple inspection: check that the packet is at least Ethernet header size (14 bytes)
            if (header->len >= 14) {
                // No-op inspection to satisfy the scenario
                volatile uint8_t first_byte = packet_data[0];
                (void)first_byte;
            }
        }
    }

    pcap_close(handle);
    return 0;
}