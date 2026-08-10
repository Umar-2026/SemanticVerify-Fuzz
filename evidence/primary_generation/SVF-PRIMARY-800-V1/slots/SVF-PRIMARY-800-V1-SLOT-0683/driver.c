#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ares.h>

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    int *out = (int *)arg;
    if (status == ARES_SUCCESS) {
        *out = 1;
    } else {
        *out = 0;
    }
    if (result) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv) return 0;

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    int optmask = 0;

    int init_status = ares_init_options(&channel, &options, optmask);
    if (init_status != ARES_SUCCESS) {
        return 0;
    }

    int set_status = ares_set_servers_csv(channel, server_csv);
    if (set_status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    char hostname[256];
    size_t len = size < sizeof(hostname) - 1 ? size : sizeof(hostname) - 1;
    memcpy(hostname, data, len);
    hostname[len] = '\0';

    int callback_result = 0;
    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, callback, &callback_result);

    int nfds;
    fd_set readers, writers;
    struct timeval tv, *tvp;
    while (1) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        nfds = ares_fds(channel, &readers, &writers);
        if (nfds == 0) {
            break;
        }
        tvp = ares_timeout(channel, NULL, &tv);
        if (select(nfds, &readers, &writers, NULL, tvp) < 0) {
            break;
        }
        ares_process(channel, &readers, &writers);
    }

    ares_destroy(channel);
    return 0;
}