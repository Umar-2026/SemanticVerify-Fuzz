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
    if (size < 10) return 0;

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
    size_t name_len = (size - 1) > 255 ? 255 : (size - 1);
    memcpy(hostname, data + 1, name_len);
    hostname[name_len] = '\0';

    struct ares_addrinfo_hints hints = {0};
    hints.ai_family = (data[0] % 2 == 0) ? AF_INET : AF_INET6;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, callback, NULL);

    struct timeval tv, *tvp;
    tvp = ares_timeout(channel, NULL, &tv);
    ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);

    ares_destroy(channel);
    return 0;
}