#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static int process_pcap(pcap_t *handle, const char *name) {
    int datalink = pcap_datalink(handle);
    if (datalink < 0) {
        fprintf(stderr, "%s: pcap_datalink failed\n", name);
        return -1;
    }
    printf("%s: datalink=%d\n", name, datalink);
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    /* Derive two independent bounded settings from input */
    size_t half = size / 2;
    size_t len1 = half;
    size_t len2 = size - half;
    if (len1 == 0 || len2 == 0) return 0;

    /* First context */
    char errbuf1[PCAP_ERRBUF_SIZE];
    pcap_t *p1 = pcap_create("lo", errbuf1);
    if (p1 == NULL) return 0;

    /* Apply bounded input-derived setting: snaplen from first byte */
    int snaplen1 = data[0] % 65536;
    if (pcap_set_snaplen(p1, snaplen1) != 0) {
        pcap_close(p1);
        return 0;
    }

    if (pcap_activate(p1) != 0) {
        pcap_close(p1);
        return 0;
    }

    /* Second context */
    char errbuf2[PCAP_ERRBUF_SIZE];
    pcap_t *p2 = pcap_create("lo", errbuf2);
    if (p2 == NULL) {
        pcap_close(p1);
        return 0;
    }

    /* Apply bounded input-derived setting: snaplen from second byte */
    int snaplen2 = data[1] % 65536;
    if (pcap_set_snaplen(p2, snaplen2) != 0) {
        pcap_close(p2);
        pcap_close(p1);
        return 0;
    }

    if (pcap_activate(p2) != 0) {
        pcap_close(p2);
        pcap_close(p1);
        return 0;
    }

    /* Inspect metadata from each */
    process_pcap(p1, "ctx1");
    process_pcap(p2, "ctx2");

    pcap_close(p2);
    pcap_close(p1);
    return 0;
}