#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

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

    char hostname[256];
    size_t host_len = (size / 2) > 255 ? 255 : (size / 2);
    memcpy(hostname, data, host_len);
    hostname[host_len] = '\0';

    struct ares_addrinfo_hints hints = {0};
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    void *callback_arg = NULL;
    ares_getaddrinfo(channel, hostname, NULL, &hints, NULL, NULL, callback_arg);

    struct timeval tv, *tvp;
    for (int i = 0; i < 5; i++) {
        tvp = ares_timeout(channel, NULL, &tv);
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
    }

    ares_destroy(channel);
    return 0;
}