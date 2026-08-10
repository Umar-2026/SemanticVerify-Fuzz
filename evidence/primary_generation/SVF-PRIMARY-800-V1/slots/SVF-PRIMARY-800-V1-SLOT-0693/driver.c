#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ares.h>

typedef struct {
    int done;
    int status;
    struct ares_addrinfo *result;
} query_state;

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    (void)timeouts;
    query_state *qs = (query_state *)arg;
    qs->done = 1;
    qs->status = status;
    qs->result = result;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    options.timeout = 2000;
    options.tries = 1;

    int status = ares_init_options(&channel, &options, ARES_OPT_FLAGS | ARES_OPT_TIMEOUT | ARES_OPT_TRIES);
    if (status != ARES_SUCCESS) return 0;

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv != NULL && server_csv[0] != '\0') {
        ares_set_servers_csv(channel, server_csv);
    }

    size_t host_len = data[0] % 64;
    if (host_len > size - 1) host_len = size - 1;
    char host[65];
    memcpy(host, data + 1, host_len);
    host[host_len] = '\0';

    query_state qs;
    memset(&qs, 0, sizeof(qs));

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, host, NULL, &hints, callback, &qs);

    int nfds;
    fd_set readers, writers;
    struct timeval tv;
    int counter = 0;
    while (!qs.done && counter < 100) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        nfds = ares_fds(channel, &readers, &writers);
        if (nfds == 0) break;
        tv.tv_sec = 0;
        tv.tv_usec = 10000;
        if (select(nfds, &readers, &writers, NULL, &tv) < 0) break;
        ares_process(channel, &readers, &writers);
        counter++;
    }

    if (qs.result != NULL) {
        ares_freeaddrinfo(qs.result);
    }
    ares_destroy(channel);
    return 0;
}