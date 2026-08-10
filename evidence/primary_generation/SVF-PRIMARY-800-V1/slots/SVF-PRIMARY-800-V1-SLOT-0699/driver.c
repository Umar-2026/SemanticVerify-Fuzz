#include <ares.h>
#include <ares_version.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>

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
    if (size < 2) return 0;

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    options.timeout = 2000;
    options.tries = 2;

    int status = ares_init_options(&channel, &options, ARES_OPT_FLAGS | ARES_OPT_TIMEOUT | ARES_OPT_TRIES);
    if (status != ARES_SUCCESS) return 0;

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv && server_csv[0]) {
        ares_set_servers_csv(channel, server_csv);
    }

    size_t name_len = data[0];
    if (name_len > size - 1) name_len = size - 1;
    if (name_len == 0) {
        ares_destroy(channel);
        return 0;
    }

    char *name = (char *)malloc(name_len + 1);
    if (!name) {
        ares_destroy(channel);
        return 0;
    }
    memcpy(name, data + 1, name_len);
    name[name_len] = '\0';

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = ARES_AI_CANONNAME;

    ares_getaddrinfo(channel, name, NULL, &hints, callback, NULL);

    int nfds = 0;
    fd_set readers, writers;
    struct timeval tv;
    for (int i = 0; i < 10; i++) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        nfds = ares_fds(channel, &readers, &writers);
        if (nfds == 0) break;
        tv.tv_sec = 0;
        tv.tv_usec = 100000;
        if (select(nfds, &readers, &writers, NULL, &tv) < 0) break;
        ares_process(channel, &readers, &writers);
    }

    free(name);
    ares_destroy(channel);
    return 0;
}