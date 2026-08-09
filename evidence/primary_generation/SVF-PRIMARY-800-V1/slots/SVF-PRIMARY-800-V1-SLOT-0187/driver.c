#include <pcap/pcap.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    // Use first byte to decide setup mode, second for activation mode, rest for packet data
    uint8_t setup_mode = data[0] % 3;
    uint8_t act_mode = data[1] % 3;
    const uint8_t *packet_data = data + 2;
    size_t packet_len = size - 2;

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *p = NULL;

    // Setup phase
    switch (setup_mode) {
        case 0:
            p = pcap_create("lo", errbuf);
            break;
        case 1:
            p = pcap_create("any", errbuf);
            break;
        case 2:
            p = pcap_create("lo0", errbuf);
            break;
        default:
            return 0;
    }

    if (p == NULL) return 0;

    // Set timeout based on data
    int timeout = (data[0] << 8) | data[1];
    if (timeout < 0) timeout = 0;
    if (timeout > 1000) timeout = 1000;
    pcap_set_timeout(p, timeout);

    // Activation phase
    int act_result;
    switch (act_mode) {
        case 0:
            act_result = pcap_activate(p);
            break;
        case 1:
            // Try to set immediate mode before activation (may fail, that's fine)
            pcap_set_immediate_mode(p, 1);
            act_result = pcap_activate(p);
            break;
        case 2:
            // Try to set buffer size before activation
            pcap_set_buffer_size(p, 65535);
            act_result = pcap_activate(p);
            break;
        default:
            act_result = pcap_activate(p);
            break;
    }

    if (act_result != 0) {
        pcap_close(p);
        return 0;
    }

    // Packet read phase: attempt to read up to 3 packets
    struct pcap_pkthdr *header;
    const u_char *pkt_data;
    int read_count = 0;
    int result;

    for (int i = 0; i < 3; i++) {
        result = pcap_next_ex(p, &header, &pkt_data);
        if (result == 1) {
            // Got a packet, process it
            read_count++;
            // Consume packet data to ensure it's used
            if (header->caplen > 0 && pkt_data != NULL) {
                volatile uint8_t sum = 0;
                size_t n = header->caplen < packet_len ? header->caplen : packet_len;
                for (size_t j = 0; j < n; j++) {
                    sum += pkt_data[j];
                }
                (void)sum;
            }
        } else if (result == 0) {
            // Timeout, stop reading
            break;
        } else if (result == -1) {
            // Error, stop reading
            break;
        } else if (result == -2) {
            // No more packets, stop reading
            break;
        }
    }

    // Distinct functional outcomes based on setup, activation, and read results
    if (setup_mode == 0 && act_mode == 0 && read_count > 0) {
        // Outcome A: loopback setup, normal activation, got packets
        pcap_close(p);
        return 1;
    } else if (setup_mode == 1 && act_mode == 1 && read_count == 0) {
        // Outcome B: any setup, immediate mode, no packets
        pcap_close(p);
        return 2;
    } else if (setup_mode == 2 && act_mode == 2 && read_count > 0) {
        // Outcome C: lo0 setup, buffer size set, got packets
        pcap_close(p);
        return 3;
    } else {
        // Outcome D: other combinations
        pcap_close(p);
        return 4;
    }
}