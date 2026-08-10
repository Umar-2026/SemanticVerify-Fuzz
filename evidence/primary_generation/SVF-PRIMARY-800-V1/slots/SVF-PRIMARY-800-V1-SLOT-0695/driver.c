#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ares.h>

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    (void)arg;
    (void)timeouts;
    if (status == ARES_SUCCESS && result) {
        struct ares_addrinfo_node *node = result->nodes;
        while (node) {
            node = node->ai_next;
        }
    }
    if (result) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;

    int optmask = ARES_OPT_FLAGS;
    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv && ares_set_servers_csv(channel, server_csv) != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    size_t name_len = data[0];
    if (name_len > size - 1) name_len = size - 1;
    char name[256];
    if (name_len >= sizeof(name)) name_len = sizeof(name) - 1;
    memcpy(name, data + 1, name_len);
    name[name_len] = '\0';

    size_t service_len = data[1];
    if (service_len > size - 2) service_len = size - 2;
    char service[64];
    if (service_len >= sizeof(service)) service_len = sizeof(service) - 1;
    memcpy(service, data + 2, service_len);
    service[service_len] = '\0';

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;
    hints.ai_flags = 0;

    ares_getaddrinfo(channel, name, service, &hints, callback, NULL);

    int nfds;
    fd_set readers, writers;
    struct timeval tv;
    for (int i = 0; i < 10; i++) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        nfds = ares_fds(channel, &readers, &writers);
        if (nfds == 0) break;
        tv.tv_sec = 0;
        tv.tv_usec = 10000;
        if (select(nfds, &readers, &writers, NULL, &tv) < 0) break;
        ares_process(channel, &readers, &writers);
    }

    ares_destroy(channel);
    return 0;
}