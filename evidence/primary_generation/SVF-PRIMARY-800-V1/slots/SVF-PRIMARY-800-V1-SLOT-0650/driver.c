#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int completed;
} user_data_t;

static void callback(void *arg, int status, int timeouts, unsigned char *abuf, int alen) {
    user_data_t *data = (user_data_t *)arg;
    data->completed = 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) return 0;

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

    char name1[64] = {0};
    char name2[64] = {0};
    size_t len1 = (size / 2) - 1;
    size_t len2 = (size / 2) - 1;
    if (len1 > 63) len1 = 63;
    if (len2 > 63) len2 = 63;

    memcpy(name1, data, len1);
    memcpy(name2, data + (size / 2), len2);

    user_data_t ctx1 = {0};
    user_data_t ctx2 = {0};

    ares_query_dnsrec(channel, name1, ARES_CLASS_IN, ARES_REC_TYPE_A, callback, &ctx1);
    ares_query_dnsrec(channel, name2, ARES_CLASS_IN, ARES_REC_TYPE_A, callback, &ctx2);

    for (int i = 0; i < 10; i++) {
        fd_set read_fds, write_fds;
        int nfds;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) break;

        struct timeval tv = {0, 10000};
        select(nfds, &read_fds, &write_fds, NULL, &tv);
        ares_process(channel, &read_fds, &write_fds);
    }

    ares_destroy(channel);
    return 0;
}