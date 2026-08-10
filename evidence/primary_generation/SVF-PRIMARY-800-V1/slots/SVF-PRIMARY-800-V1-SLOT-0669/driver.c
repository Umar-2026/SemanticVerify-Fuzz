#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <ares.h>

typedef struct {
    int done;
    int status;
    struct ares_addrinfo *result;
} lookup_state;

static void lookup_cb(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    (void)timeouts;
    lookup_state *st = (lookup_state *)arg;
    st->status = status;
    st->result = result;
    st->done = 1;
}

static void process_events(ares_channel_t *channel, int *done) {
    while (!*done) {
        int nfds;
        fd_set readers, writers;
        struct timeval tv, *tvp;
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
        ares_process_fd(channel, FD_ISSET(0, &readers) ? ARES_SOCKET_BAD : ARES_SOCKET_BAD,
                        FD_ISSET(1, &writers) ? ARES_SOCKET_BAD : ARES_SOCKET_BAD);
        ares_process(channel, &readers, &writers);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    (void)data;
    (void)size;

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv || !*server_csv) {
        return 0;
    }

    ares_channel_t *chan1 = NULL;
    ares_channel_t *chan2 = NULL;
    struct ares_options opts;
    memset(&opts, 0, sizeof(opts));
    opts.flags = ARES_FLAG_STAYOPEN;

    if (ares_init_options(&chan1, &opts, 0) != ARES_SUCCESS) {
        return 0;
    }
    if (ares_init_options(&chan2, &opts, 0) != ARES_SUCCESS) {
        ares_destroy(chan1);
        return 0;
    }

    if (ares_set_servers_csv(chan1, server_csv) != ARES_SUCCESS) {
        ares_destroy(chan1);
        ares_destroy(chan2);
        return 0;
    }
    if (ares_set_servers_csv(chan2, server_csv) != ARES_SUCCESS) {
        ares_destroy(chan1);
        ares_destroy(chan2);
        return 0;
    }

    lookup_state st1 = {0, 0, NULL};
    lookup_state st2 = {0, 0, NULL};

    const char *name1 = "example.com";
    const char *name2 = "www.example.org";

    ares_getaddrinfo(chan1, name1, NULL, NULL, lookup_cb, &st1);
    ares_getaddrinfo(chan2, name2, NULL, NULL, lookup_cb, &st2);

    while (!st1.done || !st2.done) {
        int nfds1, nfds2;
        fd_set readers1, writers1, readers2, writers2;
        struct timeval tv1, tv2, *tvp1, *tvp2;
        int max_fd = -1;

        FD_ZERO(&readers1);
        FD_ZERO(&writers1);
        FD_ZERO(&readers2);
        FD_ZERO(&writers2);

        if (!st1.done) {
            nfds1 = ares_fds(chan1, &readers1, &writers1);
            if (nfds1 > max_fd) max_fd = nfds1;
        }
        if (!st2.done) {
            nfds2 = ares_fds(chan2, &readers2, &writers2);
            if (nfds2 > max_fd) max_fd = nfds2;
        }

        if (max_fd == -1) {
            break;
        }

        tvp1 = ares_timeout(chan1, NULL, &tv1);
        tvp2 = ares_timeout(chan2, NULL, &tv2);
        struct timeval min_tv;
        if (tvp1 && tvp2) {
            min_tv = *tvp1;
            if (tvp2->tv_sec < min_tv.tv_sec ||
                (tvp2->tv_sec == min_tv.tv_sec && tvp2->tv_usec < min_tv.tv_usec)) {
                min_tv = *tvp2;
            }
        } else if (tvp1) {
            min_tv = *tvp1;
        } else if (tvp2) {
            min_tv = *tvp2;
        } else {
            min_tv.tv_sec = 0;
            min_tv.tv_usec = 100000;
        }

        fd_set read_all, write_all;
        FD_ZERO(&read_all);
        FD_ZERO(&write_all);
        if (!st1.done) {
            FD_ISSET(0, &readers1) ? FD_SET(0, &read_all) : 0;
            FD_ISSET(1, &writers1) ? FD_SET(1, &write_all) : 0;
        }
        if (!st2.done) {
            FD_ISSET(0, &readers2) ? FD_SET(0, &read_all) : 0;
            FD_ISSET(1, &writers2) ? FD_SET(1, &write_all) : 0;
        }

        if (select(max_fd + 1, &read_all, &write_all, NULL, &min_tv) < 0) {
            break;
        }

        if (!st1.done) {
            ares_process_fd(chan1, FD_ISSET(0, &read_all) ? 0 : ARES_SOCKET_BAD,
                            FD_ISSET(1, &write_all) ? 1 : ARES_SOCKET_BAD);
            ares_process(chan1, &read_all, &write_all);
        }
        if (!st2.done) {
            ares_process_fd(chan2, FD_ISSET(0, &read_all) ? 0 : ARES_SOCKET_BAD,
                            FD_ISSET(1, &write_all) ? 1 : ARES_SOCKET_BAD);
            ares_process(chan2, &read_all, &write_all);
        }
    }

    if (st1.result) {
        ares_freeaddrinfo(st1.result);
    }
    if (st2.result) {
        ares_freeaddrinfo(st2.result);
    }

    ares_destroy(chan1);
    ares_destroy(chan2);
    return 0;
}