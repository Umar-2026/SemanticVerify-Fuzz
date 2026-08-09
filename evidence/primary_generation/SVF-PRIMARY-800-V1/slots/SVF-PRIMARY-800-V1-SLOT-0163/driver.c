#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static int process_pcap_input(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    /* First context settings */
    uint32_t snaplen1 = 0;
    for (int i = 0; i < 4; i++) {
        snaplen1 = (snaplen1 << 8) | data[i];
    }
    snaplen1 %= 65536;
    if (snaplen1 == 0) snaplen1 = 65536;

    uint32_t timeout1 = 0;
    for (int i = 4; i < 8; i++) {
        timeout1 = (timeout1 << 8) | data[i];
    }
    timeout1 %= 1000;

    /* Second context settings */
    uint32_t snaplen2 = 0;
    for (int i = 8; i < 12 && i < size; i++) {
        snaplen2 = (snaplen2 << 8) | data[i];
    }
    if (size < 12) snaplen2 = 65536;
    snaplen2 %= 65536;
    if (snaplen2 == 0) snaplen2 = 65536;

    uint32_t timeout2 = 0;
    for (int i = 12; i < 16 && i < size; i++) {
        timeout2 = (timeout2 << 8) | data[i];
    }
    if (size < 16) timeout2 = 100;
    timeout2 %= 1000;

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
    pcap_set_timeout(handle1, (int)timeout1);
    pcap_set_promisc(handle1, 0);

    pcap_set_snaplen(handle2, (int)snaplen2);
    pcap_set_timeout(handle2, (int)timeout2);
    pcap_set_promisc(handle2, 0);

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

    /* Inspect metadata: use link types to influence control flow */
    volatile int result = 0;
    if (linktype1 == DLT_EN10MB) {
        result += 1;
    } else if (linktype1 == DLT_LOOP) {
        result += 2;
    } else {
        result += 3;
    }

    if (linktype2 == DLT_EN10MB) {
        result += 4;
    } else if (linktype2 == DLT_LOOP) {
        result += 8;
    } else {
        result += 16;
    }

    pcap_close(handle1);
    pcap_close(handle2);

    return result;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    process_pcap_input(data, size);
    return 0;
}