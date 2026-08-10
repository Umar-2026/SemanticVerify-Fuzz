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
    
    int timeout_ms = (data[0] << 8) | data[1];
    if (timeout_ms < 1) timeout_ms = 1;
    options.timeout = timeout_ms;

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv) {
        ares_set_servers_csv(channel, server_csv);
    }

    fuzz_context_t ctx = { .channel = channel, .completed = 0 };
    
    size_t host_len = size - 2;
    char *host = malloc(host_len + 1);
    memcpy(host, data + 2, host_len);
    host[host_len] = '\0';

    ares_getaddrinfo(channel, host, NULL, NULL, NULL, callback, &ctx);

    for (int i = 0; i < 10; i++) {
        struct timeval *tvp, tv;
        fd_set read_fds, write_fds;
        int nfds;

        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) break;

        tv.tv_sec = 0;
        tv.tv_usec = 10000;
        tvp = ares_timeout(channel, &tv, &tv);
        
        select(nfds, &read_fds, &write_fds, NULL, tvp);
        ares_process(channel, &read_fds, &write_fds);
        
        if (ctx.completed) break;
    }

    free(host);
    ares_destroy(channel);
    return 0;
}