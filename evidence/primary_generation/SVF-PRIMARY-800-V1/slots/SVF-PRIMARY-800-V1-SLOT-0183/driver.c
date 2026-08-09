#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 3) {
        return 0;
    }

    // Use first byte to select device type
    uint8_t device_type = data[0];
    // Use second byte for timeout
    uint8_t timeout_val = data[1];
    // Use third byte to decide whether to call pcap_next_ex
    uint8_t do_read = data[2];

    const char *device = NULL;
    char errbuf[PCAP_ERRBUF_SIZE];

    // Select a loopback device based on the first byte
    if (device_type % 3 == 0) {
        device = "lo";
    } else if (device_type % 3 == 1) {
        device = "lo0";
    } else {
        device = "any";
    }

    pcap_t *handle = pcap_create(device, errbuf);
    if (handle == NULL) {
        return 0;
    }

    // Set timeout
    pcap_set_timeout(handle, timeout_val);

    // Activate
    int activate_result = pcap_activate(handle);
    if (activate_result != 0) {
        pcap_close(handle);
        return 0;
    }

    // Optionally read a packet
    if (do_read % 2 == 0) {
        struct pcap_pkthdr *header;
        const u_char *packet_data;
        int next_result = pcap_next_ex(handle, &header, &packet_data);
        if (next_result == 1) {
            // Packet read successfully
            if (header->len > 0 && packet_data != NULL) {
                // Consume some bytes from the packet to ensure it's used
                volatile uint8_t sum = 0;
                size_t consume_len = header->caplen < 64 ? header->caplen : 64;
                for (size_t i = 0; i < consume_len; i++) {
                    sum += packet_data[i];
                }
                (void)sum;
            }
        } else if (next_result == 0) {
            // Timeout expired
        } else if (next_result == -1) {
            // Error
        } else if (next_result == -2) {
            // No more packets
        }
    }

    pcap_close(handle);
    return 0;
}