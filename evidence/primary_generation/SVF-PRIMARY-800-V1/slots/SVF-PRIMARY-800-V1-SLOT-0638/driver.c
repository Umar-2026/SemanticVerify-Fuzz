#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int completed;
} callback_data_t;

static void addrinfo_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    callback_data_t *data = (callback_data_t *)arg;
    data->completed = 1;
    if (status == ARES_SUCCESS && result != NULL) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    ares_channel channel;
    struct ares_options options;
    int optmask = 0;
    char *server_csv = getenv("SVF_CARES_SERVER_CSV");

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    if (server_csv) {
        ares_set_servers_csv(channel, server_csv);
    }

    size_t name_len = (size - 4) % 64;
    char *hostname = malloc(name_len + 1);
    if (!hostname) {
        ares_destroy(channel);
        return 0;
    }
    memcpy(hostname, data + 4, name_len);
    hostname[name_len] = '\0';

    callback_data_t cb_data = {0};
    struct ares_addrinfo_hints hints = {0};
    hints.ai_family = AF_UNSPEC;

    ares_getaddrinfo(channel, hostname, NULL, &hints, addrinfo_callback, &cb_data);

    struct timeval tv, *tvp;
    while (!cb_data.completed) {
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

    free(hostname);
    ares_destroy(channel);
    return 0;
}