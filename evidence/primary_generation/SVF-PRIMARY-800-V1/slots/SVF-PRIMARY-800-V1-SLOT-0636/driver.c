#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

static void addrinfo_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    (void)arg;
    (void)status;
    (void)timeouts;
    if (result) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    ares_channel channel;
    struct ares_options options;
    int optmask = 0;
    char *server_csv = getenv("SVF_CARES_SERVER_CSV");

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    if (server_csv) {
        ares_set_servers_csv(channel, server_csv);
    }

    size_t name_len = size - 1;
    char *name = malloc(name_len + 1);
    if (!name) {
        ares_destroy(channel);
        return 0;
    }
    memcpy(name, data, name_len);
    name[name_len] = '\0';

    struct ares_addrinfo_hints hints = {0};
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, name, NULL, &hints, addrinfo_callback, NULL);

    struct timeval *tvp, tv;
    fd_set read_fds, write_fds;
    int nfds;

    for (int i = 0; i < 5; i++) {
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) break;

        tvp = ares_timeout(channel, NULL, &tv);
        select(nfds, &read_fds, &write_fds, NULL, tvp);
        ares_process(channel, &read_fds, &write_fds);
    }

    free(name);
    ares_destroy(channel);
    return 0;
}