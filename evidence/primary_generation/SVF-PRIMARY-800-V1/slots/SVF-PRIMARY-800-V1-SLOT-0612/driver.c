#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    ares_channel channel;
    int completed;
} fuzz_context_t;

static void callback(void *arg, int status, int timeouts, struct addrinfo *res) {
    fuzz_context_t *ctx = (fuzz_context_t *)arg;
    ctx->completed = 1;
    if (res) {
        ares_freeaddrinfo(res);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 5) return 0;

    ares_channel channel;
    struct ares_options options;
    int optmask = ARES_OPT_TIMEOUTMS;
    
    // Use first 4 bytes for timeout configuration (0-65535 ms)
    unsigned int timeout = (data[0] << 8) | data[1];
    options.timeout = (int)timeout;

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv) {
        ares_set_servers_csv(channel, server_csv);
    }

    fuzz_context_t ctx = {channel, 0};
    
    // Use remaining data as hostname (null-terminated)
    char hostname[256];
    size_t host_len = (size - 2) > 255 ? 255 : (size - 2);
    memcpy(hostname, data + 2, host_len);
    hostname[host_len] = '\0';

    ares_getaddrinfo(channel, hostname, NULL, NULL, NULL, callback, &ctx);

    // Process until completion or timeout
    struct timeval tv, *tvp;
    while (!ctx.completed) {
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