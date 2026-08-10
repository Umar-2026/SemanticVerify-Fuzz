#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int count;
    size_t total_len;
} addr_summary_t;

static void addrinfo_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    addr_summary_t *summary = (addr_summary_t *)arg;
    if (status == ARES_SUCCESS && result && result->nodes) {
        struct ares_addrinfo_node *node = result->nodes;
        while (node) {
            summary->count++;
            if (node->ai_addr) {
                summary->total_len += node->ai_addrlen;
            }
            node = node->ai_next;
        }
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv) return 0;

    char *hostname = (char *)malloc(size + 1);
    memcpy(hostname, data, size);
    hostname[size] = '\0';

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

    addr_summary_t summary = {0, 0};
    struct ares_addrinfo_hints hints = {0};
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, addrinfo_callback, &summary);

    struct timeval tv, *tvp;
    for (int i = 0; i < 5; i++) {
        tvp = ares_timeout(channel, NULL, &tv);
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
    }

    ares_destroy(channel);
    free(hostname);
    return 0;
}