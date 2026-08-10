#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int done;
    int status;
    unsigned char *buf;
    size_t len;
} query_result;

static void query_callback(void *arg, int status, int timeouts, unsigned char *abuf, int alen) {
    query_result *res = (query_result *)arg;
    res->done = 1;
    res->status = status;
    if (status == ARES_SUCCESS && abuf && alen > 0) {
        res->buf = (unsigned char *)malloc((size_t)alen);
        if (res->buf) {
            memcpy(res->buf, abuf, (size_t)alen);
            res->len = (size_t)alen;
        }
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    /* Extract two hostname strings from fuzz input, bounded and NUL-terminated. */
    size_t len1 = data[0];
    size_t len2 = data[1];
    if (len1 > size - 2) len1 = size - 2;
    if (len2 > size - 2 - len1) len2 = size - 2 - len1;

    char name1[256];
    char name2[256];
    if (len1 >= sizeof(name1)) len1 = sizeof(name1) - 1;
    if (len2 >= sizeof(name2)) len2 = sizeof(name2) - 1;

    memcpy(name1, data + 2, len1);
    name1[len1] = '\0';
    memcpy(name2, data + 2 + len1, len2);
    name2[len2] = '\0';

    /* Ensure names are non-empty and not too long for DNS. */
    if (len1 == 0 || len2 == 0 || len1 > 253 || len2 > 253) return 0;

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv) return 0;

    ares_channel channel;
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

    query_result res1;
    query_result res2;
    memset(&res1, 0, sizeof(res1));
    memset(&res2, 0, sizeof(res2));

    ares_query_dnsrec(channel, name1, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &res1, 0);
    ares_query_dnsrec(channel, name2, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &res2, 0);

    /* Drive the event loop until both callbacks have fired. */
    int max_fd;
    fd_set read_fds, write_fds;
    struct timeval tv;
    int nfds;
    int both_done = 0;

    while (!both_done) {
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) {
            /* No sockets pending; break to avoid infinite loop. */
            break;
        }
        tv.tv_sec = 0;
        tv.tv_usec = 100000; /* 100 ms */
        max_fd = nfds;
        if (select(max_fd, &read_fds, &write_fds, NULL, &tv) < 0) {
            break;
        }
        ares_process(channel, &read_fds, &write_fds);
        if (res1.done && res2.done) {
            both_done = 1;
        }
    }

    /* Consume callback outcomes. */
    if (res1.buf) free(res1.buf);
    if (res2.buf) free(res2.buf);

    ares_destroy(channel);
    return 0;
}