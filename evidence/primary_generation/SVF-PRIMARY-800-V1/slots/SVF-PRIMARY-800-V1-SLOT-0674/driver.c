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

    char hostname[256];
    size_t name_len = (size - 1) % 255;
    memcpy(hostname, data + 1, name_len);
    hostname[name_len] = '\0';

    ares_channel_t *channel = NULL;
    struct ares_options options;
    int optmask = 0;
    int result_found = 0;
    char *server_csv = getenv("SVF_CARES_SERVER_CSV");

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    if (server_csv) {
        ares_set_servers_csv(channel, server_csv);
    }

    ares_query_dnsrec(channel, hostname, ARES_CLASS_IN, ARES_REC_TYPE_A, dns_callback, &result_found);

    struct timeval tv, *tvp;
    tvp = ares_timeout(channel, NULL, &tv);
    ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);

    ares_destroy(channel);

    return 0;
}