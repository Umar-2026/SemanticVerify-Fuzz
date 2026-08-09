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

#define BUF_SIZE 65536

static void emit_udp_packet(void) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) return;
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(9999);
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    const char *payload = "hello";
    sendto(fd, payload, strlen(payload), 0, (struct sockaddr *)&addr, sizeof(addr));
    close(fd);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    pcap_t *handle = pcap_create("lo", NULL);
    if (handle == NULL) return 0;

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    // Build a filter from the fuzz input, but keep it bounded and safe.
    // We only use the first byte to select a simple filter expression.
    char filter_expr[64];
    uint8_t selector = data[0] % 3;
    if (selector == 0) {
        snprintf(filter_expr, sizeof(filter_expr), "udp");
    } else if (selector == 1) {
        snprintf(filter_expr, sizeof(filter_expr), "udp port 9999");
    } else {
        snprintf(filter_expr, sizeof(filter_expr), "udp and src host 127.0.0.1");
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
    pcap_freecode(&fp);

    // Emit a local UDP packet to trigger capture.
    emit_udp_packet();

    // Capture a bounded number of packets.
    struct pcap_pkthdr *header;
    const u_char *packet_data;
    int packets_seen = 0;
    int timeout_ms = 100;
    struct timeval tv;
    tv.tv_sec = 0;
    tv.tv_usec = timeout_ms * 1000;

    // Use pcap_next_ex with a short timeout via pcap_set_timeout? We already activated.
    // We'll just call pcap_next_ex a few times with a small sleep between.
    for (int i = 0; i < 5; i++) {
        int ret = pcap_next_ex(handle, &header, &packet_data);
        if (ret == 1) {
            packets_seen++;
            // Process packet data minimally: just check length.
            if (header->len > 0 && packet_data != NULL) {
                // No-op to use data.
                volatile uint8_t sum = 0;
                for (uint32_t j = 0; j < header->caplen && j < 64; j++) {
                    sum += packet_data[j];
                }
                (void)sum;
            }
            if (packets_seen >= 3) break;
        } else if (ret == 0) {
            // Timeout, try again.
            usleep(10000);
        } else if (ret == -1) {
            // Error.
            break;
        } else if (ret == -2) {
            // No more packets.
            break;
        }
    }

    pcap_close(handle);
    return 0;
}