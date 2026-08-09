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

    // Determine payload size (cap at 512 bytes)
    size_t payload_len = size > 512 ? 512 : size;
    char payload[512];
    memcpy(payload, data, payload_len);

    // Send the datagram to ourselves
    struct sockaddr_in dest;
    memset(&dest, 0, sizeof(dest));
    dest.sin_family = AF_INET;
    dest.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    dest.sin_port = addr.sin_port; // same port we bound to

    if (sendto(sock, payload, payload_len, 0, (struct sockaddr *)&dest, sizeof(dest)) < 0) {
        close(sock);
        return 0;
    }

    // Set up pcap on loopback
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_create("lo", errbuf);
    if (handle == NULL) {
        close(sock);
        return 0;
    }

    // Set immediate mode to avoid buffering delays
    if (pcap_set_immediate_mode(handle, 1) != 0) {
        pcap_close(handle);
        close(sock);
        return 0;
    }

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        close(sock);
        return 0;
    }

    // Capture one packet with a short timeout
    struct pcap_pkthdr *header;
    const u_char *packet;
    int ret = pcap_next_ex(handle, &header, &packet);
    if (ret == 1) {
        // Successfully got a packet; we don't need to process it further
        (void)header;
        (void)packet;
    }

    pcap_close(handle);
    close(sock);
    return 0;
}