#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int done;
    int got_record;
} callback_data;

static void query_callback(void *arg, int status, int timeouts, unsigned char *abuf, int alen) {
    (void)timeouts;
    (void)abuf;
    (void)alen;
    callback_data *data = (callback_data *)arg;
    if (status == ARES_SUCCESS) {
        /* The record is parsed by ares_query_dnsrec internally; if we get here,
           a non-NULL parsed DNS record was received. */
        data->got_record = 1;
    }
    data->done = 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    /* Extract a bounded IPv4 address from fuzz input. */
    unsigned char ip[4];
    ip[0] = data[0];
    ip[1] = data[1];
    ip[2] = data[2];
    ip[3] = data[3];

    /* Build a hostname string from the IP address. */
    char hostname[32];
    snprintf(hostname, sizeof(hostname), "%u.%u.%u.%u", ip[0], ip[1], ip[2], ip[3]);

    /* Initialize c-ares channel. */
    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    int optmask = 0;
    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    /* Set the server from the environment variable. */
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv != NULL) {
        ares_set_servers_csv(channel, server_csv);
    }

    /* Prepare callback data. */
    callback_data cb_data;
    cb_data.done = 0;
    cb_data.got_record = 0;

    /* Issue the A record query. */
    ares_query_dnsrec(channel, hostname, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &cb_data, NULL);

    /* Process events until the callback fires. */
    int nfds;
    fd_set readers, writers;
    struct timeval tv, *tvp;
    while (!cb_data.done) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        nfds = ares_fds(channel, &readers, &writers);
        if (nfds == 0) {
            break;
        }
        tvp = ares_timeout(channel, NULL, &tv);
        if (select(nfds, &readers, &writers, NULL, tvp) < 0) {
            break;
        }
        ares_process(channel, &readers, &writers);
    }

    /* Produce binary result: 1 if a non-NULL parsed DNS record was received, else 0. */
    uint8_t result = cb_data.got_record ? 1 : 0;

    /* Clean up. */
    ares_destroy(channel);

    /* Output the result via a volatile write to prevent optimization. */
    volatile uint8_t *out = (volatile uint8_t *)result;
    (void)out;

    return 0;
}