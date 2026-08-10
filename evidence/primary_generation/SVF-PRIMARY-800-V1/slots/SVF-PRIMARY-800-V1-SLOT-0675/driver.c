#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int done;
    int got_record;
} query_state;

static void query_callback(void *arg, int status, int timeouts, unsigned char *abuf, int alen) {
    (void)timeouts;
    (void)abuf;
    (void)alen;
    query_state *state = (query_state *)arg;
    if (status == ARES_SUCCESS) {
        ares_dns_record_t *dnsrec = NULL;
        ares_status_t rv = ares_parse_dns_reply(abuf, alen, &dnsrec);
        if (rv == ARES_SUCCESS && dnsrec != NULL) {
            state->got_record = 1;
            ares_dns_record_destroy(dnsrec);
        }
    }
    state->done = 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    /* Build a hostname from fuzz input: up to 63 chars, alphanumeric + hyphen + dot */
    char name[64];
    size_t n = size < 63 ? size : 63;
    size_t i;
    for (i = 0; i < n; i++) {
        char c = (char)data[i];
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
            (c >= '0' && c <= '9') || c == '-' || c == '.') {
            name[i] = c;
        } else {
            name[i] = 'a';
        }
    }
    name[n] = '\0';

    /* Ensure the name is not empty and not just dots */
    if (n == 0 || strspn(name, ".") == n) {
        return 0;
    }

    /* Initialize c-ares channel */
    ares_channel_t *channel = NULL;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    int status = ares_init_options(&channel, &options, ARES_OPT_FLAGS);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    /* Set servers from environment variable */
    const char *servers = getenv("SVF_CARES_SERVER_CSV");
    if (servers != NULL && servers[0] != '\0') {
        ares_set_servers_csv(channel, servers);
    }

    /* Prepare query state */
    query_state state;
    state.done = 0;
    state.got_record = 0;

    /* Issue A record query */
    ares_query_dnsrec(channel, name, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &state, NULL);

    /* Run event loop until callback fires or timeout */
    int max_waits = 100;
    while (!state.done && max_waits-- > 0) {
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 10000; /* 10 ms */
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        /* Use select to wait for socket events */
        fd_set read_fds, write_fds;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        int nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) {
            /* No sockets, just wait a bit */
            struct timeval wait_tv = {0, 10000};
            select(0, NULL, NULL, NULL, &wait_tv);
        } else {
            struct timeval wait_tv = {0, 10000};
            select(nfds + 1, &read_fds, &write_fds, NULL, &wait_tv);
        }
        ares_process_fd(channel, &read_fds, &write_fds);
    }

    /* Produce binary result: 1 if got record, 0 otherwise */
    volatile uint8_t result = state.got_record ? 1 : 0;
    (void)result;

    /* Cleanup */
    ares_destroy(channel);

    return 0;
}