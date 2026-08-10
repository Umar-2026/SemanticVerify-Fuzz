#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

static void dns_callback(void *arg, ares_status_t status, size_t timeouts, const ares_dns_record_t *dnsrec) {
    (void)arg;
    (void)status;
    (void)timeouts;
    (void)dnsrec;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2 || size > 255) {
        return 0;
    }

    char *hostname = (char *)malloc(size + 1);
    if (!hostname) return 0;
    memcpy(hostname, data, size);
    hostname[size] = '\0';

    char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv) {
        free(hostname);
        return 0;
    }

    ares_channel_t *channel = NULL;
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

    ares_query_dnsrec(channel, hostname, ARES_CLASS_IN, ARES_REC_TYPE_A, 0, dns_callback, NULL, NULL);

    ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
    
    ares_destroy(channel);
    free(hostname);

    return 0;
}