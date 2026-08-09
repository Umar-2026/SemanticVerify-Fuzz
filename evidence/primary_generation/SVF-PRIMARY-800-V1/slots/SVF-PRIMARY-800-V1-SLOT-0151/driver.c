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
    addr.sin_port = htons(9999);
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

    char payload[8] = {0xde, 0xad, 0xbe, 0xef, 0x01, 0x02, 0x03, 0x04};
    int ret = sendto(fd, payload, sizeof(payload), 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
    return ret;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    // Build a bounded filter expression from fuzz input (null-terminated, bounded)
    char filter[FUZZ_FILTER_MAX];
    size_t filter_len = size < FUZZ_FILTER_MAX - 1 ? size : FUZZ_FILTER_MAX - 1;
    memcpy(filter, data, filter_len);
    filter[filter_len] = '\0';

    // Ensure the filter is bounded to "udp" or "udp port 9999" style, but we just use it as-is
    // The filter is bounded by FUZZ_FILTER_MAX and null-terminated.

    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) {
        return 0;
    }

    // Set some options to make capture work in this environment
    pcap_set_snaplen(handle, 65535);
    pcap_set_promisc(handle, 0);
    pcap_set_timeout(handle, 1000);
    pcap_set_buffer_size(handle, 1024 * 1024);

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    struct bpf_program fp;
    if (pcap_compile(handle, &fp, filter, 1, PCAP_NETMASK_UNKNOWN) != 0) {
        pcap_close(handle);
        return 0;
    }

    if (pcap_setfilter(handle, &fp) != 0) {
        pcap_freecode(&fp);
        pcap_close(handle);
        return 0;
    }

    // Send a local UDP packet to loopback
    if (send_udp_packet() < 0) {
        pcap_freecode(&fp);
        pcap_close(handle);
        return 0;
    }

    // Try to capture the packet
    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int ret = pcap_next_ex(handle, &header, &packet_data);
    if (ret == 1) {
        // Inspect the packet: just check it has some bytes
        if (header->caplen > 0 && packet_data != NULL) {
            // Simple inspection: verify the packet is non-empty
            volatile uint8_t first_byte = packet_data[0];
            (void)first_byte;
        }
    }

    pcap_freecode(&fp);
    pcap_close(handle);
    return 0;
}