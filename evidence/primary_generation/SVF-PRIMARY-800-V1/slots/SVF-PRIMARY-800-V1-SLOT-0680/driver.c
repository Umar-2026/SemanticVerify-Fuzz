#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int received;
} callback_data_t;

static void dns_callback(void *arg, int status, int timeouts, unsigned char *abuf, int alen) {
    callback_data_t *data = (callback_data_t *)arg;
    struct ares_dns_record *dnsrec = NULL;

    if (status == ARES_SUCCESS && abuf != NULL && alen > 0) {
        if (ares_parse_dns_reply(abuf, alen, NULL, &dnsrec) == ARES_SUCCESS) {
            if (dnsrec != NULL) {
                data->received = 1;
                ares_dns_record_destroy(dnsrec);
            }
        }
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1 || size > 255) {
        return 0;
    }

    char hostname[256];
    memcpy(hostname, data, size);
    hostname[size] = '\0';

    ares_channel_t *channel;
    struct ares_options options;
    int optmask = 0;
    callback_data_t cb_data = {0};
    char *server_csv = getenv("SVF_CARES_SERVER_CSV");

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    if (server_csv) {
        ares_set_servers_csv(channel, server_csv);
    }

    ares_query_dnsrec(channel, hostname, ARES_CLASS_IN, ARES_REC_TYPE_A, dns_callback, &cb_data);

    struct timeval tv, *tvp;
    while (1) {
        tvp = ares_timeout(channel, NULL, &tv);
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        if (!ares_has_queries(channel)) break;
    }

    ares_destroy(channel);
    return 0;
}