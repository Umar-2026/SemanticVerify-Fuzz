#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>
#include <sys/time.h>

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    if (status == ARES_SUCCESS && result != NULL) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) return 0;

    ares_channel channel;
    struct ares_options options;
    int optmask = ARES_OPT_FLAGS;
    
    options.flags = ARES_FLAG_NOCHECKRESP;
    
    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv) {
        ares_set_servers_csv(channel, server_csv);
    }

    char host[64];
    size_t host_len = (size / 2) > 63 ? 63 : (size / 2);
    memcpy(host, data, host_len);
    host[host_len] = '\0';

    struct ares_addrinfo_hints hints = {0};
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, host, NULL, &hints, callback, NULL);

    struct timeval tv, *tvp;
    for (int i = 0; i < 5; i++) {
        fd_set read_fds, write_fds;
        int nfds;

        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) break;

        tvp = ares_timeout(channel, NULL, &tv);
        select(nfds, &read_fds, &write_fds, NULL, tvp);
        ares_process(channel, &read_fds, &write_fds);
    }

    ares_destroy(channel);
    return 0;
}