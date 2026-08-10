#include <ares.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    (void)arg;
    (void)timeouts;
    if (status == ARES_SUCCESS && result != NULL) {
        struct ares_addrinfo_node *node = result->nodes;
        while (node != NULL) {
            node = node->ai_next;
        }
    }
    if (result != NULL) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL) {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;

    int status = ares_init_options(&channel, &options, 0);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    size_t name_len = size;
    if (name_len > 255) {
        name_len = 255;
    }
    char name[256];
    memcpy(name, data, name_len);
    name[name_len] = '\0';

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, name, NULL, &hints, callback, NULL);

    int nfds;
    fd_set readers, writers;
    struct timeval tv;
    for (int i = 0; i < 10; i++) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        nfds = ares_fds(channel, &readers, &writers);
        if (nfds == 0) {
            break;
        }
        tv.tv_sec = 0;
        tv.tv_usec = 10000;
        if (select(nfds, &readers, &writers, NULL, &tv) < 0) {
            break;
        }
        ares_process(channel, &readers, &writers);
    }

    ares_destroy(channel);
    return 0;
}