#include <pcap/pcap.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

#define MAX_PACKETS 64
#define MAX_FILTER_LEN 256

static int send_udp_packet(uint16_t port, const char *payload, size_t len) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) return -1;
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = htons(port);
    int ret = sendto(fd, payload, len, 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
    return ret;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Parse input: [2 bytes snaplen][2 bytes timeout][2 bytes filter_len][2 bytes payload_len][filter][payload]
    uint16_t snaplen = (uint16_t)(data[0] | (data[1] << 8));
    uint16_t timeout = (uint16_t)(data[2] | (data[3] << 8));
    uint16_t filter_len = (uint16_t)(data[4] | (data[5] << 8));
    uint16_t payload_len = (uint16_t)(data[6] | (data[7] << 8));

    if (filter_len > MAX_FILTER_LEN) filter_len = MAX_FILTER_LEN;
    if (payload_len > 512) payload_len = 512;
    if (snaplen > 65535) snaplen = 65535;
    if (timeout > 1000) timeout = 1000;

    size_t offset = 8;
    if (offset + filter_len + payload_len > size) return 0;

    char filter[MAX_FILTER_LEN + 1];
    memcpy(filter, data + offset, filter_len);
    filter[filter_len] = '\0';
    offset += filter_len;

    const char *payload = (const char *)(data + offset);
    size_t plen = payload_len;

    // Send a UDP packet to loopback to generate traffic
    uint16_t dst_port = 40000 + (snaplen % 1000);
    if (send_udp_packet(dst_port, payload, plen) < 0) return 0;

    // Create capture handle
    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    pcap_set_snaplen(handle, snaplen);
    pcap_set_timeout(handle, timeout);

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
    int count = 0;
    while (count < MAX_PACKETS) {
        int ret = pcap_next_ex(handle, &header, &packet_data);
        if (ret == 1) {
            // Inspect packet: check if it's UDP and matches our sent packet
            if (header->caplen >= 42) { // Ethernet + IP + UDP headers
                const uint8_t *eth = packet_data;
                uint16_t ether_type = (eth[12] << 8) | eth[13];
                if (ether_type == 0x0800) { // IPv4
                    const uint8_t *ip = eth + 14;
                    uint8_t proto = ip[9];
                    if (proto == 17) { // UDP
                        const uint8_t *udp = ip + 20;
                        uint16_t sport = (udp[0] << 8) | udp[1];
                        uint16_t dport = (udp[2] << 8) | udp[3];
                        // Just inspect, no output needed
                        (void)sport;
                        (void)dport;
                    }
                }
            }
            count++;
        } else if (ret == 0) {
            // Timeout, continue
            continue;
        } else {
            break;
        }
    }

    pcap_freecode(&fp);
    pcap_close(handle);
    return 0;
}