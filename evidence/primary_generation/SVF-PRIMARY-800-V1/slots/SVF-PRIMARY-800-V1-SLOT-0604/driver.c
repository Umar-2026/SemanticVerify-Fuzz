#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    (void)arg;
    (void)status;
    (void)timeouts;
    if (result) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4 || size > 256) {
        return 0;
    }

    char *hostname = malloc(size + 1);
    if (!hostname) return 0;
    memcpy(hostname, data, size);
    hostname[size] = '\0';

    ares_channel channel;
    struct ares_options options;
    int optmask = 0;

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        free(hostname);
        return 0;
    }

    char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv) {
        ares_set_servers_csv(channel, server_csv);
    }

    struct ares_addrinfo_hints hints = {0};
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, callback, NULL);

    struct timeval tv, *tvp;
    fd_set read_fds, write_fds;
    int nfds;

    FD_ZERO(&read_fds);
    FD_ZERO(&write_fds);
    nfds = ares_fds(channel, &read_fds, &write_fds);
    tvp = ares_timeout(channel, NULL, &tv);

    select(nfds, &read_fds, &write_fds, NULL, tvp);
    ares_process(channel, &read_fds, &write_fds);

    ares_destroy(channel);
    free(hostname);

    return 0;
}