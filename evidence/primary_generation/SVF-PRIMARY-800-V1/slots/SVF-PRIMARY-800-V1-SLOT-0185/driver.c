#include <pcap/pcap.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 3) return 0;

    // Use first byte to select device type (loopback or null)
    int use_loopback = data[0] % 2;
    const char *device = use_loopback ? "lo" : "any";

    // Use second byte for timeout value
    int timeout = data[1] % 1000;

    // Use third byte to decide whether to set a snaplen (not required, but harmless)
    // Remaining data used as packet data for pcap_next_ex buffer (not actually used)

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_create(device, errbuf);
    if (handle == NULL) {
        return 0;
    }

    // Set timeout
    if (pcap_set_timeout(handle, timeout) != 0) {
        pcap_close(handle);
        return 0;
    }

    // Activate
    int activate_result = pcap_activate(handle);
    if (activate_result != 0) {
        pcap_close(handle);
        return 0;
    }

    // Prepare a buffer for packet data
    uint8_t packet_buf[65536];
    struct pcap_pkthdr *header = NULL;
    const uint8_t *packet_data = NULL;

    // Call pcap_next_ex once
    int next_result = pcap_next_ex(handle, &header, &packet_data);

    // Distinct functional outcomes based on results
    if (next_result == 1) {
        // Got a packet: copy some bytes into packet_buf (bounded)
        if (header != NULL && packet_data != NULL) {
            size_t copy_len = header->caplen;
            if (copy_len > sizeof(packet_buf)) copy_len = sizeof(packet_buf);
            memcpy(packet_buf, packet_data, copy_len);
        }
    } else if (next_result == 0) {
        // Timeout expired, no packet
        // Do nothing specific
    } else if (next_result == -1) {
        // Error reading packet
        // Do nothing specific
    } else if (next_result == -2) {
        // No more packets (break loop)
        // Do nothing specific
    }

    pcap_close(handle);
    return 0;
}