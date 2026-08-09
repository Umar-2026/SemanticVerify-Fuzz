#include <pcap/pcap.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    // Use first byte to select setup mode
    uint8_t mode = data[0];
    const uint8_t *pkt_data = data + 1;
    size_t pkt_size = size - 1;

    // Create a pcap handle for loopback
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_create("lo", errbuf);
    if (handle == NULL) {
        return 0;
    }

    // Set timeout based on mode
    int timeout = (mode & 0x01) ? 100 : 0;
    pcap_set_timeout(handle, timeout);

    // Activate
    int act_status = pcap_activate(handle);
    if (act_status != 0) {
        pcap_close(handle);
        return 0;
    }

    // Prepare a packet buffer for pcap_next_ex
    struct pcap_pkthdr *header = NULL;
    const u_char *packet = NULL;

    // If we have packet data, attempt to inject it? No, we just read.
    // We'll call pcap_next_ex once. The result determines outcome.
    int ret = pcap_next_ex(handle, &header, &packet);

    // Distinct functional outcomes based on ret and mode
    if (ret == 1) {
        // Packet received
        if (header != NULL && packet != NULL) {
            // Consume some bytes from the packet (bounded)
            size_t consume = pkt_size;
            if (consume > header->caplen) consume = header->caplen;
            volatile uint8_t sum = 0;
            for (size_t i = 0; i < consume; i++) {
                sum += packet[i];
            }
            (void)sum;
        }
    } else if (ret == 0) {
        // Timeout expired
        // Use pkt_data to do something bounded
        volatile uint8_t sum = 0;
        size_t consume = pkt_size;
        if (consume > 64) consume = 64;
        for (size_t i = 0; i < consume; i++) {
            sum += pkt_data[i];
        }
        (void)sum;
    } else if (ret == -1) {
        // Error
        // Use mode to branch
        if (mode & 0x02) {
            // Do nothing special
        } else {
            // Consume some input
            volatile uint8_t sum = 0;
            size_t consume = pkt_size;
            if (consume > 32) consume = 32;
            for (size_t i = 0; i < consume; i++) {
                sum += pkt_data[i];
            }
            (void)sum;
        }
    } else {
        // ret == -2, PCAP_ERROR_BREAK (not expected but handle)
        // Consume all input in a bounded way
        volatile uint8_t sum = 0;
        size_t consume = pkt_size;
        if (consume > 128) consume = 128;
        for (size_t i = 0; i < consume; i++) {
            sum += pkt_data[i];
        }
        (void)sum;
    }

    pcap_close(handle);
    return 0;
}