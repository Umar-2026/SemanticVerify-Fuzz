#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int done;
    int got_record;
} query_state;

static void query_callback(void *arg, int status, int timeouts, ares_dns_record_t *dnsrec) {
    query_state *state = (query_state *)arg;
    (void)timeouts;
    if (status == ARES_SUCCESS && dnsrec != NULL) {
        state->got_record = 1;
    }
    state->done = 1;
    if (dnsrec != NULL) {
        ares_dns_record_destroy(dnsrec);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL) {
        return 0;
    }

    ares_channel_t *channel = NULL;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;

    if (ares_init_options(&channel, &options, 0) != ARES_SUCCESS) {
        return 0;
    }

    if (ares_set_servers_csv(channel, server_csv) != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    /* Build a bounded hostname from fuzz input: up to 63 chars, alphanumeric and hyphen */
    char name[64];
    size_t name_len = size > 63 ? 63 : size;
    size_t i;
    for (i = 0; i < name_len; i++) {
        char c = (char)data[i];
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '-') {
            name[i] = c;
        } else {
            name[i] = 'a';
        }
    }
    name[name_len] = '\0';

    query_state state;
    state.done = 0;
    state.got_record = 0;

    ares_dns_record_t *dnsrec = NULL;
    ares_status_t status = ares_query_dnsrec(channel, &dnsrec, name, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &state, NULL);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    /* Wait for the callback to complete (bounded by ares' internal timeouts) */
    int nfds;
    ares_pollfd_t *pollfds = NULL;
    while (!state.done) {
        if (ares_get_pollfds(channel, &pollfds, &nfds) != ARES_SUCCESS) {
            break;
        }
        if (nfds == 0) {
            break;
        }
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 100000; /* 100 ms */
        int res = ares_poll(pollfds, nfds, &tv);
        if (res < 0) {
            break;
        }
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        ares_free_pollfds(pollfds);
        pollfds = NULL;
    }
    if (pollfds != NULL) {
        ares_free_pollfds(pollfds);
    }

    /* Produce binary result: 1 if got a record, 0 otherwise */
    uint8_t result = state.got_record ? 1 : 0;
    (void)result; /* result is the fuzz output; in this harness we just return */

    ares_destroy(channel);
    return 0;
}