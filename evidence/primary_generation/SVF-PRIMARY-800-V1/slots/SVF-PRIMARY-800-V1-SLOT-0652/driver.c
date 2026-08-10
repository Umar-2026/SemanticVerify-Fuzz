#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int count;
    size_t total_len;
} summary_t;

static void addrinfo_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    summary_t *summary = (summary_t *)arg;
    if (status == ARES_SUCCESS && result != NULL && result->nodes != NULL) {
        struct ares_addrinfo_node *node = result->nodes;
        while (node != NULL) {
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
    int optmask = 0;

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        free(hostname);
        return 0;
    }

    if (ares_set_servers_csv(channel, server_csv) != ARES_SUCCESS) {
        ares_destroy(channel);
        free(hostname);
        return 0;
    }

    summary_t summary = {0, 0};
    struct ares_addrinfo_hints hints = {0};
    hints.ai_family = AF_UNSPEC;

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