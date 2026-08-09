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
#define FUZZ_FILTER_MAX 256

static int send_udp_packet(void) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) return -1;

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(9999);

    const char payload[] = "fuzz-test";
    int ret = sendto(fd, payload, sizeof(payload), 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
    return ret;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Use first byte to select filter type, rest for filter expression (bounded)
    uint8_t filter_choice = data[0];
    size_t filter_len = size - 1;
    if (filter_len > FUZZ_FILTER_MAX) filter_len = FUZZ_FILTER_MAX;

    char filter_expr[FUZZ_FILTER_MAX + 1];
    memcpy(filter_expr, data + 1, filter_len);
    filter_expr[filter_len] = '\0';

    // Ensure the filter expression is null-terminated and bounded
    // Choose a simple filter based on the first byte to keep it valid
    const char *base_filter;
    switch (filter_choice % 4) {
        case 0: base_filter = "udp"; break;
        case 1: base_filter = "udp port 9999"; break;
        case 2: base_filter = "ip"; break;
        default: base_filter = "udp and ip"; break;
    }

    // Combine base filter with fuzz bytes (but keep it simple and bounded)
    char full_filter[512];
    snprintf(full_filter, sizeof(full_filter), "%s %s", base_filter, filter_expr);

    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    struct bpf_program fp;
    if (pcap_compile(handle, &fp, full_filter, 1, PCAP_NETMASK_UNKNOWN) != 0) {
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
    int result = pcap_next_ex(handle, &header, &packet_data);
    if (result == 1) {
        // Inspect the packet (just check it's non-null and has some length)
        if (header->len > 0 && packet_data != NULL) {
            // Simple inspection: check the first byte is non-zero (Ethernet/IP header)
            if (packet_data[0] != 0) {
                // Do nothing, just exercise the code path
            }
        }
    }

    pcap_close(handle);
    return 0;
}