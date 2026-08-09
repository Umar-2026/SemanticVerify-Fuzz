#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static int process_packet(u_char *user, const struct pcap_pkthdr *h, const u_char *bytes) {
    (void)user;
    (void)bytes;
    if (h->len > 0) {
        volatile uint32_t sink = 0;
        sink += h->len;
        (void)sink;
    }
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    uint32_t snaplen1 = 0;
    uint32_t snaplen2 = 0;
    uint32_t timeout1 = 0;
    uint32_t timeout2 = 0;
    uint32_t promisc1 = 0;
    uint32_t promisc2 = 0;

    memcpy(&snaplen1, data, 4);
    memcpy(&snaplen2, data + 4, 4);
    if (size >= 12) memcpy(&timeout1, data + 8, 4);
    if (size >= 16) memcpy(&timeout2, data + 12, 4);
    if (size >= 20) promisc1 = data[16] & 1;
    if (size >= 21) promisc2 = data[17] & 1;

    if (snaplen1 == 0 || snaplen1 > 262144) snaplen1 = 65535;
    if (snaplen2 == 0 || snaplen2 > 262144) snaplen2 = 65535;
    if (timeout1 > 10000) timeout1 = 1000;
    if (timeout2 > 10000) timeout2 = 1000;

    char errbuf1[PCAP_ERRBUF_SIZE];
    char errbuf2[PCAP_ERRBUF_SIZE];
    memset(errbuf1, 0, sizeof(errbuf1));
    memset(errbuf2, 0, sizeof(errbuf2));

    pcap_t *handle1 = pcap_create("lo", errbuf1);
    pcap_t *handle2 = pcap_create("lo", errbuf2);

    if (handle1 == NULL || handle2 == NULL) {
        if (handle1) pcap_close(handle1);
        if (handle2) pcap_close(handle2);
        return 0;
    }

    pcap_set_snaplen(handle1, snaplen1);
    pcap_set_timeout(handle1, timeout1);
    pcap_set_promisc(handle1, promisc1);
    pcap_set_snaplen(handle2, snaplen2);
    pcap_set_timeout(handle2, timeout2);
    pcap_set_promisc(handle2, promisc2);

    int act1 = pcap_activate(handle1);
    int act2 = pcap_activate(handle2);

    if (act1 == 0) {
        int dl1 = pcap_datalink(handle1);
        (void)dl1;
        pcap_loop(handle1, 1, process_packet, NULL);
    }
    if (act2 == 0) {
        int dl2 = pcap_datalink(handle2);
        (void)dl2;
        pcap_loop(handle2, 1, process_packet, NULL);
    }

    if (handle1) pcap_close(handle1);
    if (handle2) pcap_close(handle2);

    return 0;
}