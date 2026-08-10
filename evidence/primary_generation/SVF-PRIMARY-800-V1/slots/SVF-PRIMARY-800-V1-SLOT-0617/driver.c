#include <ares.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    (void)arg;
    (void)status;
    (void)timeouts;
    if (result) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));

    /* Derive a bounded timeout from the first 4 bytes (0-1000 ms) */
    uint32_t raw_timeout;
    memcpy(&raw_timeout, data, 4);
    int timeout_ms = (int)(raw_timeout % 1001);
    options.timeout = timeout_ms;
    options.flags = ARES_FLAG_STAYOPEN;
    options.tries = 1;

    int status = ares_init_options(&channel, &options, ARES_OPT_TIMEOUT | ARES_OPT_FLAGS | ARES_OPT_TRIES);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv) {
        status = ares_set_servers_csv(channel, server_csv);
        if (status != ARES_SUCCESS) {
            ares_destroy(channel);
            return 0;
        }
    }

    /* Use remaining bytes to form a hostname (null-terminated, bounded) */
    size_t name_len = size - 4;
    if (name_len > 255) {
        name_len = 255;
    }
    char hostname[256];
    memcpy(hostname, data + 4, name_len);
    hostname[name_len] = '\0';

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, callback, NULL);

    /* Process events until the callback is invoked (bounded by timeout) */
    int nfds;
    fd_set readers, writers;
    struct timeval tv;
    tv.tv_sec = 0;
    tv.tv_usec = (timeout_ms > 0) ? timeout_ms * 1000 : 1000;

    for (int i = 0; i < 10; i++) {
        nfds = ares_fds(channel, &readers, &writers);
        if (nfds == 0) {
            break;
        }
        if (select(nfds, &readers, &writers, NULL, &tv) < 0) {
            break;
        }
        ares_process(channel, &readers, &writers);
        tv.tv_sec = 0;
        tv.tv_usec = (timeout_ms > 0) ? timeout_ms * 1000 : 1000;
    }

    ares_destroy(channel);
    return 0;
}