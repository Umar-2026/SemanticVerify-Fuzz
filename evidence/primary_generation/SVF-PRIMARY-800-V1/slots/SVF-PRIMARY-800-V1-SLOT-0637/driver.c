#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <ares.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/socket.h>

typedef struct {
    int pending;
    int failures;
    int successes;
} lookup_state;

static void addr_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    lookup_state *state = (lookup_state *)arg;
    (void)timeouts;
    if (status == ARES_SUCCESS && result != NULL) {
        state->successes++;
        struct ares_addrinfo_node *node = result->nodes;
        while (node != NULL) {
            node = node->ai_next;
        }
        ares_freeaddrinfo(result);
    } else {
        state->failures++;
    }
    state->pending--;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL || server_csv[0] == '\0') {
        return 0;
    }

    if (size < 1) {
        return 0;
    }

    /* Bound the number of lookups to avoid excessive work */
    size_t max_lookups = 16;
    size_t num_lookups = (size_t)data[0] % max_lookups;
    if (num_lookups == 0) {
        num_lookups = 1;
    }

    /* Extract hostname candidates from fuzz input, each NUL-terminated */
    char hostnames[16][256];
    size_t host_count = 0;
    size_t offset = 1;
    while (host_count < num_lookups && offset < size) {
        size_t len = 0;
        while (offset + len < size && data[offset + len] != '\0' && len < 255) {
            len++;
        }
        if (len == 0) {
            break;
        }
        memcpy(hostnames[host_count], data + offset, len);
        hostnames[host_count][len] = '\0';
        host_count++;
        offset += len + 1;
    }

    if (host_count == 0) {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    int status = ares_init_options(&channel, &options, 0);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    lookup_state state;
    memset(&state, 0, sizeof(state));
    state.pending = 0;

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    for (size_t i = 0; i < host_count; i++) {
        ares_getaddrinfo(channel, hostnames[i], NULL, &hints, addr_callback, &state);
        state.pending++;
    }

    /* Process until all callbacks have fired or a timeout */
    int numfds;
    fd_set readers, writers;
    struct timeval tv;
    while (state.pending > 0) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        numfds = ares_fds(channel, &readers, &writers);
        if (numfds == 0) {
            break;
        }
        tv.tv_sec = 0;
        tv.tv_usec = 1000; /* 1 ms */
        if (select(numfds, &readers, &writers, NULL, &tv) < 0) {
            break;
        }
        ares_process(channel, &readers, &writers);
    }

    ares_destroy(channel);
    return 0;
}