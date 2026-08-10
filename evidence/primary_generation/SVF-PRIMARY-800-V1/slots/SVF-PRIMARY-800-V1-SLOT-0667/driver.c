#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>
#include <ares_version.h>

static void addr_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    int *done = (int *)arg;
    (void)timeouts;
    if (status == ARES_SUCCESS && result) {
        /* consume result by walking the nodes */
        struct ares_addrinfo_node *node = result->nodes;
        while (node) {
            node = node->ai_next;
        }
        ares_freeaddrinfo(result);
    }
    *done = 1;
}

int main(int argc, char **argv) {
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv || !*server_csv) {
        server_csv = "127.0.0.1";
    }

    ares_channel_t *chan1 = NULL;
    ares_channel_t *chan2 = NULL;
    struct ares_options opts;
    int optmask = 0;
    int status;

    memset(&opts, 0, sizeof(opts));
    /* Use default options; we only need to set servers later */
    status = ares_init_options(&chan1, &opts, optmask);
    if (status != ARES_SUCCESS) {
        return 1;
    }
    status = ares_init_options(&chan2, &opts, optmask);
    if (status != ARES_SUCCESS) {
        ares_destroy(chan1);
        return 1;
    }

    status = ares_set_servers_csv(chan1, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(chan1);
        ares_destroy(chan2);
        return 1;
    }
    status = ares_set_servers_csv(chan2, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(chan1);
        ares_destroy(chan2);
        return 1;
    }

    int done1 = 0, done2 = 0;

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    /* Issue one bounded lookup on each channel */
    ares_getaddrinfo(chan1, "example.com", NULL, &hints, addr_callback, &done1);
    ares_getaddrinfo(chan2, "example.org", NULL, &hints, addr_callback, &done2);

    /* Drive both channels until both callbacks have fired */
    while (!done1 || !done2) {
        ares_channel_t *chans[2];
        int nfds = 0;
        struct timeval tv, *tvp;
        fd_set read_fds, write_fds;
        int i;

        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);

        chans[0] = chan1;
        chans[1] = chan2;

        for (i = 0; i < 2; i++) {
            ares_socket_t socks[ARES_GETSOCK_MAXNUM];
            int bitmask = ares_getsock(chans[i], socks, ARES_GETSOCK_MAXNUM);
            int j;
            for (j = 0; j < ARES_GETSOCK_MAXNUM; j++) {
                if (bitmask & (ARES_GETSOCK_READABLE(j))) {
                    FD_SET(socks[j], &read_fds);
                    if (socks[j] >= nfds) nfds = socks[j] + 1;
                }
                if (bitmask & (ARES_GETSOCK_WRITABLE(j))) {
                    FD_SET(socks[j], &write_fds);
                    if (socks[j] >= nfds) nfds = socks[j] + 1;
                }
            }
        }

        tvp = ares_timeout(chans[0], NULL, &tv);
        if (!tvp) {
            tvp = ares_timeout(chans[1], NULL, &tv);
        } else {
            struct timeval tv2;
            struct timeval *tvp2 = ares_timeout(chans[1], NULL, &tv2);
            if (tvp2 && (tvp2->tv_sec < tvp->tv_sec ||
                         (tvp2->tv_sec == tvp->tv_sec && tvp2->tv_usec < tvp->tv_usec))) {
                tvp = tvp2;
            }
        }

        if (nfds == 0 && tvp == NULL) {
            /* No sockets and no timeout; avoid infinite loop */
            break;
        }

        if (select(nfds, &read_fds, &write_fds, NULL, tvp) < 0) {
            break;
        }

        for (i = 0; i < 2; i++) {
            ares_socket_t socks[ARES_GETSOCK_MAXNUM];
            int bitmask = ares_getsock(chans[i], socks, ARES_GETSOCK_MAXNUM);
            int j;
            for (j = 0; j < ARES_GETSOCK_MAXNUM; j++) {
                if (bitmask & (ARES_GETSOCK_READABLE(j))) {
                    if (FD_ISSET(socks[j], &read_fds)) {
                        ares_process_fd(chans[i], socks[j], ARES_SOCKET_BAD);
                    }
                }
                if (bitmask & (ARES_GETSOCK_WRITABLE(j))) {
                    if (FD_ISSET(socks[j], &write_fds)) {
                        ares_process_fd(chans[i], ARES_SOCKET_BAD, socks[j]);
                    }
                }
            }
        }
    }

    ares_destroy(chan1);
    ares_destroy(chan2);
    return 0;
}