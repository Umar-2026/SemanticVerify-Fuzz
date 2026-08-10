#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *res) {
    (void)arg;
    (void)status;
    (void)timeouts;
    if (res) {
        ares_freeaddrinfo(res);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) return 0;

    char *hostname = (char *)malloc(size + 1);
    memcpy(hostname, data, size);
    hostname[size] = '\0';

    ares_channel channel1, channel2;
    struct ares_options options;
    int optmask = ARES_OPT_FLAGS;
    options.flags = ARES_FLAG_NOCHECKRESP;

    if (ares_init_options(&channel1, &options, optmask) != ARES_SUCCESS) {
        free(hostname);
        return 0;
    }
    if (ares_init_options(&channel2, &options, optmask) != ARES_SUCCESS) {
        ares_destroy(channel1);
        free(hostname);
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv) {
        ares_set_servers_csv(channel1, server_csv);
        ares_set_servers_csv(channel2, server_csv);
    }

    ares_getaddrinfo(channel1, hostname, NULL, NULL, NULL, callback, NULL);
    ares_getaddrinfo(channel2, hostname, NULL, NULL, NULL, callback, NULL);

    fd_set read_fds, write_fds;
    struct timeval tv, *tvp;
    int nfds;

    for (int i = 0; i < 5; i++) {
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        nfds = ares_fds(channel1, &read_fds, &write_fds);
        nfds = ares_fds(channel2, &read_fds, &write_fds);
        if (nfds == 0) break;

        tvp = ares_timeout(channel1, NULL, &tv);
        tvp = ares_timeout(channel2, tvp, &tv);
        select(nfds, &read_fds, &write_fds, NULL, tvp);
        ares_process(channel1, &read_fds, &write_fds);
        ares_process(channel2, &read_fds, &write_fds);
    }

    ares_destroy(channel1);
    ares_destroy(channel2);
    free(hostname);

    return 0;
}