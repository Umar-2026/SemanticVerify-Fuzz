#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <net/if.h>
#include <sys/socket.h>
#include <unistd.h>
#include <errno.h>

#define MAX_FILTER_LEN 256
#define MAX_PACKETS 100
#define MAX_SNAPLEN 65535

static int emit_udp_packet(uint16_t src_port, uint16_t dst_port, const uint8_t *payload, size_t payload_len) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) return -1;
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(dst_port);
    int sent = sendto(fd, payload, payload_len, 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
    return (sent == (int)payload_len) ? 0 : -1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Input-derived capture settings
    uint16_t snaplen = (uint16_t)(data[0] | (data[1] << 8));
    if (snaplen == 0 || snaplen > MAX_SNAPLEN) snaplen = 65535;
    int timeout_ms = (int)(data[2] | (data[3] << 8));
    if (timeout_ms < 0) timeout_ms = 0;
    if (timeout_ms > 1000) timeout_ms = 1000;

    // Build filter expression from input (bounded)
    char filter[MAX_FILTER_LEN];
    size_t filter_len = data[4] % (MAX_FILTER_LEN - 1);
    if (filter_len > size - 5) filter_len = size - 5;
    memcpy(filter, data + 5, filter_len);
    filter[filter_len] = '\0';

    // Ensure filter is a valid expression: if empty, use "udp"
    if (filter_len == 0) {
        strcpy(filter, "udp");
    }

    // Emit a local UDP packet to capture (payload from input)
    size_t payload_len = size - 5 - filter_len;
    if (payload_len > 512) payload_len = 512;
    uint16_t src_port = 40000 + (data[5] % 1000);
    uint16_t dst_port = 50000 + (data[6] % 1000);
    const uint8_t *payload = data + 5 + filter_len;
    if (payload_len > 0) {
        emit_udp_packet(src_port, dst_port, payload, payload_len);
    }

    // Set up capture on loopback
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
    if (pcap_compile(handle, &fp, filter, 1, PCAP_NETMASK_UNKNOWN) != 0) {
        pcap_close(handle);
        return 0;
    }
    if (pcap_setfilter(handle, &fp) != 0) {
        pcap_freecode(&fp);
        pcap_close(handle);
        return 0;
    }

    // Capture a bounded number of packets
    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int packets_seen = 0;
    int result;
    while (packets_seen < MAX_PACKETS) {
        result = pcap_next_ex(handle, &header, &packet_data);
        if (result == 1) {
            // Inspect UDP packet: parse IP header
            if (header->caplen >= sizeof(struct ip)) {
                struct ip *iph = (struct ip *)packet_data;
                if (iph->ip_p == IPPROTO_UDP && header->caplen >= (size_t)(iph->ip_hl * 4 + sizeof(struct udphdr))) {
                    struct udphdr *udph = (struct udphdr *)(packet_data + iph->ip_hl * 4);
                    // Just read ports to ensure inspection
                    (void)ntohs(udph->uh_sport);
                    (void)ntohs(udph->uh_dport);
                }
            }
            packets_seen++;
        } else if (result == 0) {
            // Timeout, stop
            break;
        } else {
            // Error or break
            break;
        }
    }

    pcap_freecode(&fp);
    pcap_close(handle);
    return 0;
}