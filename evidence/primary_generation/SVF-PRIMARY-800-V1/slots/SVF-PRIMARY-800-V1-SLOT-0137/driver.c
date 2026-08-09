#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/udp.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>

#define MAX_PACKETS 16
#define MAX_PAYLOAD 512

static int build_udp_packet(uint8_t *buf, size_t buf_len, const uint8_t *payload, size_t payload_len) {
    if (buf_len < sizeof(struct ip) + sizeof(struct udphdr) + payload_len) {
        return -1;
    }
    struct ip *iph = (struct ip *)buf;
    struct udphdr *udph = (struct udphdr *)(buf + sizeof(struct ip));
    uint8_t *data = buf + sizeof(struct ip) + sizeof(struct udphdr);

    memset(iph, 0, sizeof(struct ip));
    iph->ip_v = 4;
    iph->ip_hl = 5;
    iph->ip_tos = 0;
    iph->ip_len = htons(sizeof(struct ip) + sizeof(struct udphdr) + payload_len);
    iph->ip_id = htons(0x1234);
    iph->ip_off = 0;
    iph->ip_ttl = 64;
    iph->ip_p = IPPROTO_UDP;
    iph->ip_sum = 0;
    iph->ip_src.s_addr = htonl(0x7f000001);
    iph->ip_dst.s_addr = htonl(0x7f000001);

    udph->uh_sport = htons(12345);
    udph->uh_dport = htons(54321);
    udph->uh_ulen = htons(sizeof(struct udphdr) + payload_len);
    udph->uh_sum = 0;

    memcpy(data, payload, payload_len);
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    size_t num_packets = data[0] % MAX_PACKETS;
    if (num_packets == 0) num_packets = 1;
    size_t offset = 1;

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return 0;

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(0x7f000001);
    addr.sin_port = htons(54321);

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(sock);
        return 0;
    }

    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) {
        close(sock);
        return 0;
    }

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        close(sock);
        return 0;
    }

    for (size_t i = 0; i < num_packets && offset < size; i++) {
        size_t payload_len = data[offset] % (MAX_PAYLOAD + 1);
        offset++;
        if (payload_len > size - offset) {
            payload_len = size - offset;
        }

        uint8_t packet[sizeof(struct ip) + sizeof(struct udphdr) + MAX_PAYLOAD];
        if (build_udp_packet(packet, sizeof(packet), data + offset, payload_len) == 0) {
            sendto(sock, data + offset, payload_len, 0, (struct sockaddr *)&addr, sizeof(addr));
        }
        offset += payload_len;
    }

    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int result = pcap_next_ex(handle, &header, &packet_data);
    if (result == 1) {
        // Inspect the captured packet
        if (header->caplen >= sizeof(struct ip)) {
            struct ip *iph = (struct ip *)packet_data;
            if (iph->ip_p == IPPROTO_UDP && header->caplen >= sizeof(struct ip) + sizeof(struct udphdr)) {
                struct udphdr *udph = (struct udphdr *)(packet_data + sizeof(struct ip));
                // Just read the fields to exercise the API
                volatile uint16_t sport = ntohs(udph->uh_sport);
                volatile uint16_t dport = ntohs(udph->uh_dport);
                (void)sport;
                (void)dport;
            }
        }
    }

    pcap_close(handle);
    close(sock);
    return 0;
}