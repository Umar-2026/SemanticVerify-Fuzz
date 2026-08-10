#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int done;
    int status;
    unsigned char *buf;
    int len;
} query_result;

static void query_callback(void *arg, int status, int timeouts, unsigned char *abuf, int alen) {
    query_result *res = (query_result *)arg;
    res->done = 1;
    res->status = status;
    res->buf = (unsigned char *)malloc(alen > 0 ? alen : 1);
    if (res->buf) {
        res->len = alen;
        if (alen > 0) {
            memcpy(res->buf, abuf, alen);
        }
    } else {
        res->len = 0;
    }
    (void)timeouts;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    int optmask = ARES_OPT_FLAGS;

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv != NULL) {
        ares_set_servers_csv(channel, server_csv);
    }

    // Derive two hostnames from fuzz input.
    // Use first half for name1, second half for name2.
    size_t half = size / 2;
    size_t len1 = half;
    size_t len2 = size - half;

    // Ensure names are null-terminated and bounded.
    char name1[256];
    char name2[256];
    if (len1 >= sizeof(name1)) len1 = sizeof(name1) - 1;
    if (len2 >= sizeof(name2)) len2 = sizeof(name2) - 1;
    memcpy(name1, data, len1);
    name1[len1] = '\0';
    memcpy(name2, data + half, len2);
    name2[len2] = '\0';

    query_result res1;
    query_result res2;
    memset(&res1, 0, sizeof(res1));
    memset(&res2, 0, sizeof(res2));

    ares_query_dnsrec(channel, name1, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &res1, NULL);
    ares_query_dnsrec(channel, name2, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &res2, NULL);

    // Process until both callbacks have fired.
    int max_waits = 1000;
    while ((!res1.done || !res2.done) && max_waits-- > 0) {
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
    }

    // Consume results.
    if (res1.buf) {
        free(res1.buf);
    }
    if (res2.buf) {
        free(res2.buf);
    }

    ares_destroy(channel);
    return 0;
}