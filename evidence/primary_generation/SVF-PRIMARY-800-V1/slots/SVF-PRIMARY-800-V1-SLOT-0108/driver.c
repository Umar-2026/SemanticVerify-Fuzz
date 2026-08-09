#include <pcap.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/udp.h>
#include <netinet/ip.h>
#include <unistd.h>
#include <arpa/inet.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1 || size > 1400) return 0;

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_create("lo", errbuf);
    if (!handle) return 0;

    pcap_set_snaplen(handle, 65535);
    pcap_set_promisc(handle, 1);
    pcap_set_timeout(handle, 100);
    
    if (pcap_activate(handle) != 0) {
        pcap_close(handle);
        return 0;
    }

    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd >= 0) {
        struct sockaddr_in addr;
        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_port = htons(12345);
        addr.sin_addr.s_addr = inet_addr("127.0.0.1");

        sendto(sockfd, data, size, 0, (struct sockaddr *)&addr, sizeof(addr));
        close(sockfd);
    }

    struct pcap_pkthdr *header;
    const u_char *pkt_data;
    int res = pcap_next_ex(handle, &header, &pkt_data);

    pcap_close(handle);
    return 0;
}