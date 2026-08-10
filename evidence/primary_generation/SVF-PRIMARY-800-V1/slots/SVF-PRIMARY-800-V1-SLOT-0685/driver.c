#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ares.h>

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    int *out = (int *)arg;
    if (status == ARES_SUCCESS && result != NULL) {
        *out = 1;
        ares_freeaddrinfo(result);
    } else {
        *out = 0;
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    int optmask = ARES_OPT_FLAGS;

    int init_status = ares_init_options(&channel, &options, optmask);
    if (init_status != ARES_SUCCESS) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv != NULL) {
        ares_set_servers_csv(channel, server_csv);
    }

    char hostname[256];
    size_t len = size < sizeof(hostname) - 1 ? size : sizeof(hostname) - 1;
    memcpy(hostname, data, len);
    hostname[len] = '\0';

    int callback_status = 0;
    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, callback, &callback_status);

    int nfds;
    fd_set readers, writers;
    struct timeval tv, *tvp;
    while (1) {
        nfds = ares_fds(channel, &readers, &writers);
        if (nfds == 0) break;
        tv.tv_sec = 0;
        tv.tv_usec = 1000;
        tvp = &tv;
        int res = select(nfds, &readers, &writers, NULL, tvp);
        if (res < 0) break;
        ares_process(channel, &readers, &writers);
    }

    ares_destroy(channel);
    return 0;
}