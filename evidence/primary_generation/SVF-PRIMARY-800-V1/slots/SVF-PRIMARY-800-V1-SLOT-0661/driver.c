#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>

typedef struct {
    int done;
    int status;
    struct ares_addrinfo *result;
} lookup_state;

static void lookup_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    lookup_state *state = (lookup_state *)arg;
    state->done = 1;
    state->status = status;
    state->result = result;
}

static void wait_ares(ares_channel channel, lookup_state *state) {
    while (!state->done) {
        fd_set read_fds, write_fds;
        int nfds;
        struct timeval tv, *tvp;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) {
            break;
        }
        tvp = ares_timeout(channel, NULL, &tv);
        if (select(nfds, &read_fds, &write_fds, NULL, tvp) < 0) {
            break;
        }
        ares_process(channel, &read_fds, &write_fds);
    }
}

int main(int argc, char *argv[]) {
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL || server_csv[0] == '\0') {
        fprintf(stderr, "SVF_CARES_SERVER_CSV not set\n");
        return 1;
    }

    if (ares_library_init(ARES_LIB_INIT_ALL) != ARES_SUCCESS) {
        fprintf(stderr, "ares_library_init failed\n");
        return 1;
    }

    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;

    ares_channel channel1, channel2;
    int status;

    status = ares_init_options(&channel1, &options, 0);
    if (status != ARES_SUCCESS) {
        fprintf(stderr, "ares_init_options channel1 failed: %s\n", ares_strerror(status));
        ares_library_cleanup();
        return 1;
    }

    status = ares_init_options(&channel2, &options, 0);
    if (status != ARES_SUCCESS) {
        fprintf(stderr, "ares_init_options channel2 failed: %s\n", ares_strerror(status));
        ares_destroy(channel1);
        ares_library_cleanup();
        return 1;
    }

    status = ares_set_servers_csv(channel1, server_csv);
    if (status != ARES_SUCCESS) {
        fprintf(stderr, "ares_set_servers_csv channel1 failed: %s\n", ares_strerror(status));
        ares_destroy(channel2);
        ares_destroy(channel1);
        ares_library_cleanup();
        return 1;
    }

    status = ares_set_servers_csv(channel2, server_csv);
    if (status != ARES_SUCCESS) {
        fprintf(stderr, "ares_set_servers_csv channel2 failed: %s\n", ares_strerror(status));
        ares_destroy(channel2);
        ares_destroy(channel1);
        ares_library_cleanup();
        return 1;
    }

    lookup_state state1 = {0, 0, NULL};
    lookup_state state2 = {0, 0, NULL};

    const char *name1 = "example.com";
    const char *name2 = "www.example.org";

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel1, name1, NULL, &hints, lookup_callback, &state1);
    ares_getaddrinfo(channel2, name2, NULL, &hints, lookup_callback, &state2);

    while (!state1.done || !state2.done) {
        fd_set read_fds, write_fds;
        int nfds1, nfds2, nfds;
        struct timeval tv, *tvp;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        nfds1 = ares_fds(channel1, &read_fds, &write_fds);
        nfds2 = ares_fds(channel2, &read_fds, &write_fds);
        nfds = (nfds1 > nfds2) ? nfds1 : nfds2;
        if (nfds == 0) {
            break;
        }
        tvp = ares_timeout(channel1, NULL, &tv);
        struct timeval tv2, *tvp2;
        tvp2 = ares_timeout(channel2, NULL, &tv2);
        if (tvp2 != NULL && (tvp == NULL || tvp2->tv_sec < tvp->tv_sec ||
            (tvp2->tv_sec == tvp->tv_sec && tvp2->tv_usec < tvp->tv_usec))) {
            tv = *tvp2;
            tvp = &tv;
        }
        if (select(nfds, &read_fds, &write_fds, NULL, tvp) < 0) {
            break;
        }
        ares_process(channel1, &read_fds, &write_fds);
        ares_process(channel2, &read_fds, &write_fds);
    }

    if (state1.result != NULL) {
        ares_freeaddrinfo(state1.result);
    }
    if (state2.result != NULL) {
        ares_freeaddrinfo(state2.result);
    }

    ares_destroy(channel2);
    ares_destroy(channel1);
    ares_library_cleanup();

    if (state1.status != ARES_SUCCESS || state2.status != ARES_SUCCESS) {
        fprintf(stderr, "lookup failed: %s / %s\n", ares_strerror(state1.status), ares_strerror(state2.status));
        return 1;
    }

    return 0;
}