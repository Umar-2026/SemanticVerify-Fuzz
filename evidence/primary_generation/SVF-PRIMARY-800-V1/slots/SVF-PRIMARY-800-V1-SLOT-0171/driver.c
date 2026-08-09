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

#define LOOPBACK_IFACE "lo"
#define SNAP_LEN 65535
#define TIMEOUT_MS 100
#define MAX_PACKETS 10
#define UDP_PORT 54321

static void emit_udp_packet(void) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) return;
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(UDP_PORT);
    const char *payload = "fuzz";
    sendto(fd, payload, strlen(payload), 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    (void)data;
    (void)size;

    pcap_t *handle = pcap_create(LOOPBACK_IFACE, NULL);
    if (handle == NULL) return 0;

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    struct bpf_program fp;
    char filter_expr[64];
    snprintf(filter_expr, sizeof(filter_expr), "udp and port %d", UDP_PORT);

    if (pcap_compile(handle, &fp, filter_expr, 1, PCAP_NETMASK_UNKNOWN) != 0) {
        pcap_close(handle);
        return 0;
    }

    if (pcap_setfilter(handle, &fp) != 0) {
        pcap_freecode(&fp);
        pcap_close(handle);
        return 0;
    }

    emit_udp_packet();

    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int packets_seen = 0;
    while (packets_seen < MAX_PACKETS) {
        int ret = pcap_next_ex(handle, &header, &packet_data);
        if (ret == 1) {
            packets_seen++;
            if (packets_seen >= 1) break;
        } else if (ret == 0) {
            continue;
        } else {
            break;
        }
    }

    pcap_freecode(&fp);
    pcap_close(handle);
    return 0;
}