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
#include <stdio.h>

#define MAX_PACKETS 64
#define MAX_SNAPLEN 65535

static int udp_packet_seen = 0;

static void process_packet(const uint8_t *packet, struct pcap_pkthdr *hdr) {
    if (hdr->caplen < sizeof(struct ip)) return;
    const struct ip *iph = (const struct ip *)packet;
    if (iph->ip_v != 4) return;
    size_t ip_hlen = iph->ip_hl * 4;
    if (ip_hlen < sizeof(struct ip) || hdr->caplen < ip_hlen + sizeof(struct udphdr)) return;
    if (iph->ip_p != IPPROTO_UDP) return;
    const struct udphdr *udph = (const struct udphdr *)(packet + ip_hlen);
    uint16_t dport = ntohs(udph->uh_dport);
    if (dport == 9999) {
        udp_packet_seen = 1;
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    uint16_t snaplen = (uint16_t)(data[0] | (data[1] << 8));
    if (snaplen == 0) snaplen = 64;
    if (snaplen > MAX_SNAPLEN) snaplen = MAX_SNAPLEN;

    int timeout = (int)(data[2] | (data[3] << 8));
    if (timeout < 0) timeout = 0;
    if (timeout > 1000) timeout = 1000;

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_create("lo", errbuf);
    if (handle == NULL) return 0;

    pcap_set_snaplen(handle, snaplen);
    pcap_set_timeout(handle, timeout);
    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    // Build a filter from input bytes (bounded to first 64 bytes after header)
    size_t filter_len = size > 68 ? 64 : size - 4;
    char filter_expr[65];
    if (filter_len > 0) {
        memcpy(filter_expr, data + 4, filter_len);
    }
    filter_expr[filter_len] = '\0';

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

    // Create a UDP socket and send a packet to loopback to generate traffic
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        pcap_close(handle);
        return 0;
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(9999);

    // Send a small UDP payload
    const char payload[] = "test";
    sendto(sock, payload, sizeof(payload), 0, (struct sockaddr *)&addr, sizeof(addr));
    close(sock);

    // Capture a bounded number of packets
    udp_packet_seen = 0;
    for (int i = 0; i < MAX_PACKETS; i++) {
        struct pcap_pkthdr *hdr;
        const uint8_t *pkt;
        int ret = pcap_next_ex(handle, &hdr, &pkt);
        if (ret == 1) {
            process_packet(pkt, hdr);
            if (udp_packet_seen) break;
        } else if (ret == 0) {
            // timeout, continue
            continue;
        } else {
            break;
        }
    }

    pcap_close(handle);
    return 0;
}