#include <pcap/pcap.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 64) {
        return 0;
    }

    pcap_t *handle1 = NULL;
    pcap_t *handle2 = NULL;
    char errbuf[PCAP_ERRBUF_SIZE];

    handle1 = pcap_create("lo", errbuf);
    handle2 = pcap_create("lo", errbuf);

    if (!handle1 || !handle2) {
        if (handle1) pcap_close(handle1);
        if (handle2) pcap_close(handle2);
        return 0;
    }

    int snaplen1 = 64 + (data[0] % 1024);
    int snaplen2 = 64 + (data[1] % 1024);
    int promisc1 = data[2] % 2;
    int promisc2 = data[3] % 2;

    pcap_set_snaplen(handle1, snaplen1);
    pcap_set_promisc(handle1, promisc1);
    pcap_set_timeout(handle1, 100);

    pcap_set_snaplen(handle2, snaplen2);
    pcap_set_promisc(handle2, promisc2);
    pcap_set_timeout(handle2, 100);

    if (pcap_activate(handle1) == 0) {
        int dl1 = pcap_datalink(handle1);
        (void)dl1;
    }

    if (pcap_activate(handle2) == 0) {
        int dl2 = pcap_datalink(handle2);
        (void)dl2;
    }

    pcap_close(handle1);
    pcap_close(handle2);

    return 0;
}