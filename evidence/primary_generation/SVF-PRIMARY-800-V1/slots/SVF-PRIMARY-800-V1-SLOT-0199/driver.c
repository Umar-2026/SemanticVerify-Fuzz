#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <sys/socket.h>
#include <unistd.h>
#include <errno.h>

#define MAX_PACKETS 64
#define MAX_FILTER_LEN 256

static int emit_udp_packet(uint16_t sport, uint16_t dport, const uint8_t *payload, size_t payload_len) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) return -1;

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(dport);

    ssize_t sent = sendto(fd, payload, payload_len, 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
    return (sent == (ssize_t)payload_len) ? 0 : -1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Input-derived capture settings
    uint16_t snaplen = (uint16_t)(data[0] | (data[1] << 8));
    if (snaplen < 64) snaplen = 64;
    if (snaplen > 65535) snaplen = 65535;

    int timeout_ms = (int)(data[2] | (data[3] << 8));
    if (timeout_ms < 0) timeout_ms = 0;
    if (timeout_ms > 1000) timeout_ms = 1000;

    // Bounded filter expression from input
    char filter_expr[MAX_FILTER_LEN];
    size_t filter_len = data[4] % (MAX_FILTER_LEN - 1);
    if (filter_len > size - 5) filter_len = size - 5;
    memcpy(filter_expr, data + 5, filter_len);
    filter_expr[filter_len] = '\0';

    // UDP emission parameters
    uint16_t sport = (uint16_t)(data[5 + filter_len] | (data[6 + filter_len] << 8));
    uint16_t dport = (uint16_t)(data[7 + filter_len] | (data[8 + filter_len] << 8));
    size_t payload_len = size - (9 + filter_len);
    if (payload_len > 512) payload_len = 512;
    const uint8_t *payload = data + 9 + filter_len;

    // Emit local UDP traffic
    if (emit_udp_packet(sport, dport, payload, payload_len) != 0) return 0;

    // Capture pipeline
    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    if (pcap_set_snaplen(handle, snaplen) != 0) {
        pcap_close(handle);
        return 0;
    }
    if (pcap_set_timeout(handle, timeout_ms) != 0) {
        pcap_close(handle);
        return 0;
    }
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

    // Bounded capture loop
    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int packets_seen = 0;
    while (packets_seen < MAX_PACKETS) {
        int ret = pcap_next_ex(handle, &header, &packet_data);
        if (ret == 1) {
            packets_seen++;
            // Inspect UDP header if present
            if (header->caplen >= sizeof(struct ip) + sizeof(struct udphdr)) {
                struct ip *iph = (struct ip *)(void *)packet_data;
                if (iph->ip_p == IPPROTO_UDP) {
                    struct udphdr *udp = (struct udphdr *)(void *)(packet_data + (iph->ip_hl * 4));
                    // Volatile read to prevent optimization
                    volatile uint16_t src = ntohs(udp->uh_sport);
                    volatile uint16_t dst = ntohs(udp->uh_dport);
                    (void)src;
                    (void)dst;
                }
            }
        } else if (ret == 0) {
            // Timeout expired
            break;
        } else {
            // Error or PCAP_ERROR_BREAK
            break;
        }
    }

    pcap_freecode(&fp);
    pcap_close(handle);
    return 0;
}