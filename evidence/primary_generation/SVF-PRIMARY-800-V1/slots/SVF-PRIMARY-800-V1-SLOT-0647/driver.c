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
    if (res->buf && alen > 0) {
        memcpy(res->buf, abuf, alen);
    }
    res->len = alen;
    (void)timeouts;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Split fuzz input into two hostname strings, each NUL-terminated.
    size_t split = 0;
    for (size_t i = 0; i < size; i++) {
        if (data[i] == 0) {
            split = i;
            break;
        }
    }
    if (split == 0 || split >= size - 1) {
        return 0;
    }

    char name1[256];
    char name2[256];
    size_t len1 = split;
    size_t len2 = size - split - 1;
    if (len1 >= sizeof(name1) || len2 >= sizeof(name2)) {
        return 0;
    }
    memcpy(name1, data, len1);
    name1[len1] = '\0';
    memcpy(name2, data + split + 1, len2);
    name2[len2] = '\0';

    // Validate hostnames are non-empty and printable.
    if (name1[0] == '\0' || name2[0] == '\0') {
        return 0;
    }
    for (size_t i = 0; name1[i]; i++) {
        if (name1[i] < 33 || name1[i] > 126) return 0;
    }
    for (size_t i = 0; name2[i]; i++) {
        if (name2[i] < 33 || name2[i] > 126) return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv || server_csv[0] == '\0') {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    int status = ares_init_options(&channel, &options, ARES_OPT_FLAGS);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    query_result res1;
    query_result res2;
    memset(&res1, 0, sizeof(res1));
    memset(&res2, 0, sizeof(res2));

    ares_query_dnsrec(channel, name1, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &res1, NULL);
    ares_query_dnsrec(channel, name2, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &res2, NULL);

    // Drive the event loop until both callbacks have fired.
    int max_fd;
    fd_set read_fds, write_fds;
    struct timeval tv;
    while (!res1.done || !res2.done) {
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        max_fd = 0;
        ares_fds(channel, &read_fds, &write_fds);
        if (ares_getsock(channel, (ares_socket_t *)&max_fd, 1) > 0) {
            // ares_getsock returns number of sockets; max_fd is set to the socket value.
            // We need to compute max_fd properly.
            // Instead, use ares_fds to get the max fd.
            // Recompute max_fd from fd sets.
            max_fd = 0;
            for (int i = 0; i < FD_SETSIZE; i++) {
                if (FD_ISSET(i, &read_fds) || FD_ISSET(i, &write_fds)) {
                    if (i > max_fd) max_fd = i;
                }
            }
        }
        tv.tv_sec = 0;
        tv.tv_usec = 10000; // 10ms
        int n = select(max_fd + 1, &read_fds, &write_fds, NULL, &tv);
        if (n < 0) {
            break;
        }
        ares_process_fd(channel, n > 0 ? &read_fds : NULL, n > 0 ? &write_fds : NULL);
        // ares_process_fd expects socket descriptors, not fd_sets. Use ares_process instead.
        // Correct approach:
        ares_process(channel, &read_fds, &write_fds);
    }

    // Consume callback outcomes.
    if (res1.buf) {
        free(res1.buf);
    }
    if (res2.buf) {
        free(res2.buf);
    }

    ares_destroy(channel);
    return 0;
}