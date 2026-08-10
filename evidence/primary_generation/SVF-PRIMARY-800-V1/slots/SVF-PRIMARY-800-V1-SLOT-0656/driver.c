#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int count;
    size_t total_len;
} lookup_summary_t;

static void addrinfo_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    lookup_summary_t *summary = (lookup_summary_t *)arg;
    if (status == ARES_SUCCESS && result && result->nodes) {
        struct ares_addrinfo_node *node = result->nodes;
        while (node) {
            summary->count++;
            summary->total_len += node->ai_addrlen;
            node = node->ai_next;
        }
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    char *hostname = (char *)malloc(size + 1);
    memcpy(hostname, data, size);
    hostname[size] = '\0';

    char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv) server_csv = "127.0.0.1";

    ares_channel channel;
    struct ares_options options;
    int optmask = ARES_OPT_FLAGS;
    options.flags = ARES_FLAG_NOCHECKRESP;

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        free(hostname);
        return 0;
    }

    if (ares_set_servers_csv(channel, server_csv) != ARES_SUCCESS) {
        ares_destroy(channel);
        free(hostname);
        return 0;
    }

    lookup_summary_t summary = {0, 0};
    ares_getaddrinfo(channel, hostname, NULL, NULL, NULL, addrinfo_callback, &summary);

    struct timeval tv, *tvp;
    while (1) {
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
    free(hostname);
    return 0;
}