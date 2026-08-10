#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int pending;
    int success;
    int failure;
} query_state;

static void query_callback(void *arg, int status, int timeouts, unsigned char *abuf, int alen) {
    query_state *qs = (query_state *)arg;
    (void)timeouts;
    (void)abuf;
    (void)alen;
    if (qs == NULL) {
        return;
    }
    if (status == ARES_SUCCESS) {
        qs->success++;
    } else {
        qs->failure++;
    }
    qs->pending--;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    /* Split fuzz input into two hostname strings, each bounded and NUL-terminated. */
    size_t half = size / 2;
    size_t len1 = half;
    size_t len2 = size - half;
    if (len1 == 0 || len2 == 0) {
        return 0;
    }

    /* Ensure room for NUL terminators. */
    char *name1 = (char *)malloc(len1 + 1);
    char *name2 = (char *)malloc(len2 + 1);
    if (name1 == NULL || name2 == NULL) {
        free(name1);
        free(name2);
        return 0;
    }

    memcpy(name1, data, len1);
    name1[len1] = '\0';
    memcpy(name2, data + half, len2);
    name2[len2] = '\0';

    /* Initialize c-ares channel. */
    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    int optmask = 0;

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        free(name1);
        free(name2);
        return 0;
    }

    /* Set server from environment variable. */
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv != NULL && server_csv[0] != '\0') {
        ares_set_servers_csv(channel, server_csv);
    }

    query_state qs1;
    query_state qs2;
    memset(&qs1, 0, sizeof(qs1));
    memset(&qs2, 0, sizeof(qs2));
    qs1.pending = 1;
    qs2.pending = 1;

    /* Issue two A-record queries. */
    ares_query_dnsrec(channel, name1, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &qs1);
    ares_query_dnsrec(channel, name2, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &qs2);

    /* Drive the event loop until both callbacks have fired. */
    int total_pending = 2;
    while (total_pending > 0) {
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 1000; /* 1 ms */
        fd_set read_fds, write_fds;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        int nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) {
            /* No sockets to wait on; break to avoid infinite loop. */
            break;
        }
        if (select(nfds, &read_fds, &write_fds, NULL, &tv) < 0) {
            break;
        }
        ares_process(channel, &read_fds, &write_fds);
        total_pending = qs1.pending + qs2.pending;
    }

    /* Consume callback outcomes (prevent unused warnings). */
    (void)qs1.success;
    (void)qs1.failure;
    (void)qs2.success;
    (void)qs2.failure;

    /* Cleanup. */
    ares_destroy(channel);
    free(name1);
    free(name2);
    return 0;
}