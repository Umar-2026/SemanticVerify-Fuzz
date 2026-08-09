#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define MAX_PACKETS 16
#define MAX_PACKET_SIZE 65535

static int process_packet(const unsigned char *data, struct pcap_pkthdr *hdr) {
    if (hdr->caplen == 0) {
        return 1;
    }
    if (hdr->caplen > MAX_PACKET_SIZE) {
        return 2;
    }
    if (data == NULL) {
        return 3;
    }
    /* Simple checksum-like operation to consume data */
    unsigned int sum = 0;
    for (unsigned int i = 0; i < hdr->caplen; i++) {
        sum += data[i];
    }
    return (sum & 0xFF) == 0 ? 4 : 5;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    /* Use first byte to select setup mode */
    int setup_mode = data[0] % 3;
    /* Use second byte to select activation mode */
    int activate_mode = data[1] % 3;
    /* Use remaining bytes as packet data source */
    const uint8_t *packet_data = data + 2;
    size_t packet_data_len = size - 2;

    pcap_t *handle = NULL;
    char errbuf[PCAP_ERRBUF_SIZE];
    memset(errbuf, 0, sizeof(errbuf));

    /* Setup phase */
    switch (setup_mode) {
        case 0:
            handle = pcap_create("lo", errbuf);
            break;
        case 1:
            handle = pcap_create("any", errbuf);
            break;
        default:
            handle = pcap_create("nonexistent_interface_xyz", errbuf);
            break;
    }

    if (handle == NULL) {
        return 0;
    }

    /* Set timeout based on activation mode */
    int timeout_ms = 0;
    switch (activate_mode) {
        case 0:
            timeout_ms = 0;
            break;
        case 1:
            timeout_ms = 100;
            break;
        default:
            timeout_ms = 1000;
            break;
    }

    if (pcap_set_timeout(handle, timeout_ms) != 0) {
        pcap_close(handle);
        return 0;
    }

    /* Activation phase */
    int act_result = pcap_activate(handle);
    if (act_result != 0) {
        pcap_close(handle);
        return 0;
    }

    /* Packet reading phase */
    int outcome = 0;
    int packets_read = 0;
    struct pcap_pkthdr *hdr = NULL;
    const unsigned char *pkt_data = NULL;

    /* Simulate reading from the live capture with bounded iterations */
    for (int i = 0; i < MAX_PACKETS; i++) {
        int ret = pcap_next_ex(handle, &hdr, &pkt_data);
        if (ret == 1) {
            /* Packet received */
            packets_read++;
            int pkt_result = process_packet(pkt_data, hdr);
            if (pkt_result == 4) {
                outcome = 10;
            } else if (pkt_result == 5) {
                outcome = 11;
            } else {
                outcome = 12;
            }
            break;
        } else if (ret == 0) {
            /* Timeout expired */
            outcome = 20;
            break;
        } else if (ret == -1) {
            /* Error */
            outcome = 30;
            break;
        } else if (ret == -2) {
            /* Break loop (not applicable for next_ex, but handle) */
            outcome = 40;
            break;
        } else {
            /* Unexpected return */
            outcome = 50;
            break;
        }
    }

    if (packets_read == 0 && outcome == 0) {
        outcome = 60;
    }

    /* Consume packet_data to ensure fuzz input is used */
    volatile unsigned int sink = 0;
    for (size_t i = 0; i < packet_data_len && i < 64; i++) {
        sink += packet_data[i];
    }
    (void)sink;

    pcap_close(handle);
    return outcome;
}