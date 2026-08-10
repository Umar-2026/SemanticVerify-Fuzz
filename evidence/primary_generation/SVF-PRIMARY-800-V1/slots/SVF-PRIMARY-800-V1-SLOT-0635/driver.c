#include <ares.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/time.h>
#endif

typedef struct {
    int pending;
    int failures;
    int successes;
    int total;
} query_state;

static void dns_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    query_state *qs = (query_state *)arg;
    qs->pending--;

    if (status == ARES_SUCCESS && result != NULL) {
        qs->successes++;
        ares_freeaddrinfo(result);
    } else {
        qs->failures++;
    }
}

static void process_events(ares_channel channel) {
    int nfds, count;
    fd_set readers, writers;
    struct timeval tv, *tvp;
    time_t now;

    for (;;) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        nfds = ares_fds(channel, &readers, &writers);
        if (nfds == 0) {
            break;
        }

        tvp = ares_timeout(channel, NULL, &tv);
        if (tvp == NULL) {
            tv.tv_sec = 0;
            tv.tv_usec = 100000;
            tvp = &tv;
        }

        count = select(nfds, &readers, &writers, NULL, tvp);
        if (count < 0) {
            break;
        }

        ares_process(channel, &readers, &writers);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL || server_csv[0] == '\0') {
        return 0;
    }

    if (size < 1) {
        return 0;
    }

    /* Bound the number of lookups to avoid excessive work */
    size_t max_lookups = 16;
    size_t num_lookups = (size_t)data[0] % max_lookups + 1;

    /* Extract hostname candidates from fuzz input, bounded */
    char hostname[256];
    size_t host_len = size - 1;
    if (host_len > sizeof(hostname) - 1) {
        host_len = sizeof(hostname) - 1;
    }
    memcpy(hostname, data + 1, host_len);
    hostname[host_len] = '\0';

    /* Ensure hostname is non-empty and printable-ish */
    if (host_len == 0) {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    options.timeout = 2000;
    options.tries = 1;

    int status = ares_init_options(&channel, &options, ARES_OPT_FLAGS | ARES_OPT_TIMEOUT | ARES_OPT_TRIES);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    query_state qs;
    memset(&qs, 0, sizeof(qs));
    qs.total = (int)num_lookups;

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    for (size_t i = 0; i < num_lookups; i++) {
        qs.pending++;
        ares_getaddrinfo(channel, hostname, NULL, &hints, dns_callback, &qs);
    }

    process_events(channel);

    ares_destroy(channel);

    return 0;
}