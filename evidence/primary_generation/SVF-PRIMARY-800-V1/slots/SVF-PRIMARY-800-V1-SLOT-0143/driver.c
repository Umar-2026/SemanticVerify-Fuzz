#include <pcap/pcap.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_create("lo", errbuf);
    if (handle == NULL) {
        return 0;
    }

    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    // Query a capture property: datalink type
    int dl = pcap_datalink(handle);
    (void)dl;

    // Inspect locally generated packet data using pcap_next_ex
    // We'll use the fuzz input to determine how many packets to attempt to read (bounded).
    // The actual packet data comes from the loopback interface, not from fuzz input.
    size_t attempts = (size_t)data[0] % 4; // bounded 0-3
    for (size_t i = 0; i < attempts; i++) {
        struct pcap_pkthdr *header;
        const u_char *packet;
        int ret = pcap_next_ex(handle, &header, &packet);
        if (ret != 1) {
            // No packet or error; stop
            break;
        }
        // Inspect packet data: just touch the first byte if available
        if (header->caplen > 0) {
            volatile uint8_t b = packet[0];
            (void)b;
        }
    }

    pcap_close(handle);
    return 0;
}