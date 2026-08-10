#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

static void dns_callback(void *arg, ares_status_t status, size_t timeouts, const ares_dns_record_t *dnsrec) {
    int *result_found = (int *)arg;
    if (status == ARES_SUCCESS && dnsrec != NULL) {
        *result_found = 1;
    } else {
        *result_found = 0;
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv) return 0;

    ares_channel_t *channel = NULL;
    struct ares_options options;
    int optmask = 0;
    int result_found = 0;

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    if (ares_set_servers_csv(channel, server_csv) != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    char hostname[256];
    size_t name_len = (size - 1) > 255 ? 255 : (size - 1);
    memcpy(hostname, data + 1, name_len);
    hostname[name_len] = '\0';

    ares_query_dnsrec(channel, hostname, ARES_CLASS_IN, ARES_REC_TYPE_A, 0, dns_callback, &result_found);

    struct timeval tv, *tvp;
    while (1) {
        tvp = ares_timeout(channel, NULL, &tv);
        fd_set read_fds, write_fds;
        int nfds;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) break;

        struct timeval wait = {0, 1000};
        select(nfds, &read_fds, &write_fds, NULL, &wait);
        ares_process(channel, &read_fds, &write_fds);
    }

    ares_destroy(channel);
    return 0;
}