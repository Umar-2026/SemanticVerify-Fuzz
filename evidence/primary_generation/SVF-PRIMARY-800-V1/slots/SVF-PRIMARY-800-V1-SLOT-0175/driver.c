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

#define MAX_PACKETS 10
#define SNAP_LEN 65535
#define TIMEOUT_MS 1000

static void emit_udp_packet(void) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) return;
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(9999);
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    const char *payload = "fuzz";
    sendto(fd, payload, 4, 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    if (pcap_set_snaplen(handle, SNAP_LEN) != 0) {
        pcap_close(handle);
        return 0;
    }
    if (pcap_set_promisc(handle, 0) != 0) {
        pcap_close(handle);
        return 0;
    }
    if (pcap_set_timeout(handle, TIMEOUT_MS) != 0) {
        pcap_close(handle);
        return 0;
    }

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    // Build a filter program from fuzz input (bounded)
    char filter_expr[128];
    size_t len = size < sizeof(filter_expr) - 1 ? size : sizeof(filter_expr) - 1;
    memcpy(filter_expr, data, len);
    filter_expr[len] = '\0';

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

    // Emit a local UDP packet to trigger capture
    emit_udp_packet();

    // Capture a bounded number of packets
    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int packets_seen = 0;
    while (packets_seen < MAX_PACKETS) {
        int ret = pcap_next_ex(handle, &header, &packet_data);
        if (ret == 1) {
            packets_seen++;
            // Inspect packet data (bounded)
            if (header->caplen > 0) {
                volatile uint8_t first_byte = packet_data[0];
                (void)first_byte;
            }
        } else if (ret == 0) {
            // Timeout, continue
            continue;
        } else {
            // Error or EOF
            break;
        }
    }

    pcap_close(handle);
    return 0;
}