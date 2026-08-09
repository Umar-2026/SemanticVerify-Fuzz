#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    // Create a UDP socket bound to loopback
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return 0;

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    addr.sin_port = 0; // ephemeral port

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(sock);
        return 0;
    }

    // Get the assigned port
    socklen_t addr_len = sizeof(addr);
    if (getsockname(sock, (struct sockaddr *)&addr, &addr_len) < 0) {
        close(sock);
        return 0;
    }

    // Prepare payload from fuzz input (limit to reasonable size)
    size_t payload_len = size;
    if (payload_len > 1400) payload_len = 1400; // keep within UDP payload limits

    // Send the datagram to ourselves
    struct sockaddr_in dest;
    memset(&dest, 0, sizeof(dest));
    dest.sin_family = AF_INET;
    dest.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    dest.sin_port = addr.sin_port;

    ssize_t sent = sendto(sock, data, payload_len, 0, (struct sockaddr *)&dest, sizeof(dest));
    if (sent < 0) {
        close(sock);
        return 0;
    }

    // Set up libpcap on loopback
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *pcap = pcap_create("lo", errbuf);
    if (pcap == NULL) {
        close(sock);
        return 0;
    }

    // Set immediate mode to avoid buffering delays
    if (pcap_set_immediate_mode(pcap, 1) != 0) {
        pcap_close(pcap);
        close(sock);
        return 0;
    }

    if (pcap_activate(pcap) != 0) {
        pcap_close(pcap);
        close(sock);
        return 0;
    }

    // Set a filter to only capture UDP packets to our port
    char filter[64];
    snprintf(filter, sizeof(filter), "udp and dst port %d", ntohs(addr.sin_port));
    struct bpf_program fp;
    if (pcap_compile(pcap, &fp, filter, 1, PCAP_NETMASK_UNKNOWN) != 0) {
        pcap_close(pcap);
        close(sock);
        return 0;
    }
    if (pcap_setfilter(pcap, &fp) != 0) {
        pcap_freecode(&fp);
        pcap_close(pcap);
        close(sock);
        return 0;
    }
    pcap_freecode(&fp);

    // Capture one packet with a timeout
    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int ret = pcap_next_ex(pcap, &header, &packet_data);
    if (ret == 1) {
        // Successfully got a packet; we don't need to do anything with it
        // The packet data is available but we just verify capture worked
    }

    pcap_close(pcap);
    close(sock);
    return 0;
}