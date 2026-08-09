#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static int process_packet(const struct pcap_pkthdr *hdr, const uint8_t *data) {
    (void)hdr;
    (void)data;
    return 0;
}

int LLVMF_FuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) {
        return 0;
    }

    // First context settings from first 4 bytes
    uint32_t snaplen1 = 0;
    for (int i = 0; i < 4; i++) {
        snaplen1 = (snaplen1 << 8) | data[i];
    }
    if (snaplen1 < 64 || snaplen1 > 65535) {
        snaplen1 = 65535;
    }

    // Second context settings from next 4 bytes
    uint32_t snaplen2 = 0;
    for (int i = 4; i < 8; i++) {
        snaplen2 = (snaplen2 << 8) | data[i];
    }
    if (snaplen2 < 64 || snaplen2 > 65535) {
        snaplen2 = 65535;
    }

    char errbuf1[PCAP_ERRBUF_SIZE];
    char errbuf2[PCAP_ERRBUF_SIZE];
    memset(errbuf1, 0, sizeof(errbuf1));
    memset(errbuf2, 0, sizeof(errbuf2));

    pcap_t *handle1 = pcap_create("lo", errbuf1);
    if (handle1 == NULL) {
        return 0;
    }

    pcap_t *handle2 = pcap_create("lo", errbuf2);
    if (handle2 == NULL) {
        pcap_close(handle1);
        return 0;
    }

    pcap_set_snaplen(handle1, (int)snaplen1);
    pcap_set_promisc(handle1, 0);
    pcap_set_timeout(handle1, 1000);

    pcap_set_snaplen(handle2, (int)snaplen2);
    pcap_set_promisc(handle2, 0);
    pcap_set_timeout(handle2, 1000);

    int status1 = pcap_activate(handle1);
    int status2 = pcap_activate(handle2);

    if (status1 == PCAP_ERROR || status1 == PCAP_ERROR_ACTIVATED) {
        pcap_close(handle1);
        pcap_close(handle2);
        return 0;
    }

    if (status2 == PCAP_ERROR || status2 == PCAP_ERROR_ACTIVATED) {
        pcap_close(handle1);
        pcap_close(handle2);
        return 0;
    }

    int linktype1 = pcap_datalink(handle1);
    int linktype2 = pcap_datalink(handle2);

    // Use the link types to influence processing
    if (linktype1 == linktype2) {
        // Both same link type, process a few packets from first
        struct pcap_pkthdr *hdr;
        const uint8_t *pkt_data;
        int result = pcap_next_ex(handle1, &hdr, &pkt_data);
        if (result == 1) {
            process_packet(hdr, pkt_data);
        }
    } else {
        // Different link types, process from second
        struct pcap_pkthdr *hdr;
        const uint8_t *pkt_data;
        int result = pcap_next_ex(handle2, &hdr, &pkt_data);
        if (result == 1) {
            process_packet(hdr, pkt_data);
        }
    }

    pcap_close(handle1);
    pcap_close(handle2);

    return 0;
}