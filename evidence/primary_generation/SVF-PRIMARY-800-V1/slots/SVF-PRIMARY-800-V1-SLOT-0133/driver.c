#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>

#define MAX_DATAGRAMS 16
#define MAX_DATAGRAM_SIZE 2048

static int build_datagram(const uint8_t *data, size_t size, uint8_t *out, size_t out_cap) {
    if (size < 8) return -1;
    size_t payload_len = size - 8;
    if (payload_len > out_cap - 42) return -1;

    /* Ethernet header (14 bytes) */
    memset(out, 0, 14);
    out[12] = 0x08;
    out[13] = 0x00;

    /* IPv4 header (20 bytes) */
    out[14] = 0x45;
    out[15] = 0x00;
    uint16_t total_len = 20 + 8 + payload_len;
    out[16] = (total_len >> 8) & 0xFF;
    out[17] = total_len & 0xFF;
    out[18] = 0x00;
    out[19] = 0x00;
    out[20] = 0x40;
    out[21] = 0x00;
    out[22] = 0x40;
    out[23] = 17; /* UDP */
    out[24] = 0x00;
    out[25] = 0x00;
    /* src 127.0.0.1 */
    out[26] = 127;
    out[27] = 0;
    out[28] = 0;
    out[29] = 1;
    /* dst 127.0.0.1 */
    out[30] = 127;
    out[31] = 0;
    out[32] = 0;
    out[33] = 1;

    /* UDP header (8 bytes) */
    out[34] = 0x04;
    out[35] = 0xD2; /* src port 1234 */
    out[36] = 0x04;
    out[37] = 0xD2; /* dst port 1234 */
    uint16_t udp_len = 8 + payload_len;
    out[38] = (udp_len >> 8) & 0xFF;
    out[39] = udp_len & 0xFF;
    out[40] = 0x00;
    out[41] = 0x00;

    memcpy(out + 42, data + 8, payload_len);
    return 42 + payload_len;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    uint8_t datagram[MAX_DATAGRAM_SIZE + 42];
    int dgram_len = build_datagram(data, size, datagram, sizeof(datagram));
    if (dgram_len < 0) return 0;

    /* Create loopback capture handle */
    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    /* Open a UDP socket to send the datagram to loopback */
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        pcap_close(handle);
        return 0;
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(1234);
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

    /* Send the payload portion (after the 8-byte fuzz header) as a UDP datagram */
    size_t payload_len = size - 8;
    if (payload_len > 0) {
        ssize_t sent = sendto(sock, data + 8, payload_len, 0,
                              (struct sockaddr *)&addr, sizeof(addr));
        if (sent < 0) {
            close(sock);
            pcap_close(handle);
            return 0;
        }
    }

    /* Capture a bounded number of packets */
    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int captured = 0;
    for (int i = 0; i < MAX_DATAGRAMS; i++) {
        int ret = pcap_next_ex(handle, &header, &packet_data);
        if (ret == 1) {
            /* Inspect the packet: just check it's non-null and has a plausible length */
            if (header->len > 0 && packet_data != NULL) {
                captured++;
            }
        } else if (ret == 0) {
            /* Timeout, continue */
            continue;
        } else {
            /* Error or EOF */
            break;
        }
    }

    close(sock);
    pcap_close(handle);
    return 0;
}