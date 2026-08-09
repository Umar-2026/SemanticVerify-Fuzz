#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    /* Use first 4 bytes for first context settings, next 4 for second */
    uint32_t snaplen1 = 0;
    uint32_t snaplen2 = 0;
    memcpy(&snaplen1, data, 4);
    memcpy(&snaplen2, data + 4, 4);

    /* Bound the snaplen values to reasonable range */
    if (snaplen1 > 65535) snaplen1 = 65535;
    if (snaplen2 > 65535) snaplen2 = 65535;

    /* Create two independent loopback capture contexts */
    pcap_t *handle1 = pcap_create("lo", NULL);
    pcap_t *handle2 = pcap_create("lo", NULL);

    if (handle1 == NULL || handle2 == NULL) {
        if (handle1) pcap_close(handle1);
        if (handle2) pcap_close(handle2);
        return 0;
    }

    /* Set snaplen from fuzz input */
    if (pcap_set_snaplen(handle1, snaplen1) != 0) {
        pcap_close(handle1);
        pcap_close(handle2);
        return 0;
    }
    if (pcap_set_snaplen(handle2, snaplen2) != 0) {
        pcap_close(handle1);
        pcap_close(handle2);
        return 0;
    }

    /* Activate both contexts */
    int status1 = pcap_activate(handle1);
    int status2 = pcap_activate(handle2);

    /* Inspect metadata from each activated context */
    if (status1 >= 0) {
        int linktype1 = pcap_datalink(handle1);
        (void)linktype1;
    }
    if (status2 >= 0) {
        int linktype2 = pcap_datalink(handle2);
        (void)linktype2;
    }

    /* Cleanup */
    pcap_close(handle1);
    pcap_close(handle2);

    return 0;
}