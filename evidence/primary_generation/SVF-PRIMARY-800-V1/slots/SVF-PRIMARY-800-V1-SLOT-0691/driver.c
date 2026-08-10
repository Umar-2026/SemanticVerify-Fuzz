#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ares.h>

typedef struct {
    int done;
    int status;
    struct ares_addrinfo *result;
} query_state;

static void query_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    query_state *state = (query_state *)arg;
    state->done = 1;
    state->status = status;
    state->result = result;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    /* Extract query settings from input */
    uint8_t qname_len = data[0];
    uint8_t qtype = data[1];
    if (qname_len == 0 || qname_len > size - 2) return 0;

    char qname[256];
    if (qname_len >= sizeof(qname)) return 0;
    memcpy(qname, data + 2, qname_len);
    qname[qname_len] = '\0';

    /* Ensure the name is null-terminated and printable-ish */
    for (int i = 0; i < qname_len; i++) {
        if (qname[i] == '\0' || qname[i] == '\n' || qname[i] == '\r') {
            qname[i] = '.';
        }
    }

    /* Initialize c-ares */
    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    int optmask = ARES_OPT_FLAGS;

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    /* Set DNS servers from environment variable */
    const char *servers = getenv("SVF_CARES_SERVER_CSV");
    if (servers != NULL && servers[0] != '\0') {
        ares_set_servers_csv(channel, servers);
    }

    /* Prepare query */
    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    if (qtype == 1) {
        hints.ai_family = AF_INET;
    } else if (qtype == 2) {
        hints.ai_family = AF_INET6;
    }

    query_state state;
    memset(&state, 0, sizeof(state));

    /* Start async getaddrinfo */
    ares_getaddrinfo(channel, qname, NULL, &hints, query_callback, &state);

    /* Run event loop with bounded iterations */
    int max_waits = 100;
    while (!state.done && max_waits-- > 0) {
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 1000; /* 1ms */
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        /* Actually need to wait for events; use select-like approach */
        fd_set read_fds, write_fds;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        int nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) {
            /* No sockets, maybe done or error */
            ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
            break;
        }
        struct timeval wait_tv = tv;
        select(nfds, &read_fds, &write_fds, NULL, &wait_tv);
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        /* Process actual ready fds */
        for (int fd = 0; fd < nfds; fd++) {
            if (FD_ISSET(fd, &read_fds) || FD_ISSET(fd, &write_fds)) {
                ares_process_fd(channel, fd, fd);
            }
        }
    }

    /* Consume result */
    if (state.done && state.result != NULL) {
        struct ares_addrinfo_node *node = state.result->nodes;
        while (node != NULL) {
            /* Touch the address data to force consumption */
            if (node->ai_addr != NULL && node->ai_addrlen > 0) {
                volatile unsigned char sink = ((unsigned char *)node->ai_addr)[0];
                (void)sink;
            }
            node = node->ai_next;
        }
        ares_freeaddrinfo(state.result);
    }

    /* Cleanup */
    ares_destroy(channel);
    return 0;
}