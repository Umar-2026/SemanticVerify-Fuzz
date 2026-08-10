#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ares.h>

#define MAX_LOOKUPS 16
#define MAX_HOSTNAME_LEN 256

typedef struct {
    ares_channel channel;
    int pending;
    int total;
    int failures;
} lookup_state;

static void dns_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    lookup_state *state = (lookup_state *)arg;
    (void)timeouts;

    if (status != ARES_SUCCESS) {
        state->failures++;
        fprintf(stderr, "Lookup failed: %s\n", ares_strerror(status));
    } else {
        struct ares_addrinfo_node *node = result->nodes;
        while (node != NULL) {
            char addr[INET6_ADDRSTRLEN] = {0};
            if (node->ai_family == AF_INET) {
                struct sockaddr_in *sin = (struct sockaddr_in *)node->ai_addr;
                inet_ntop(AF_INET, &sin->sin_addr, addr, sizeof(addr));
            } else if (node->ai_family == AF_INET6) {
                struct sockaddr_in6 *sin6 = (struct sockaddr_in6 *)node->ai_addr;
                inet_ntop(AF_INET6, &sin6->sin6_addr, addr, sizeof(addr));
            }
            if (addr[0] != '\0') {
                printf("Resolved: %s\n", addr);
            }
            node = node->ai_next;
        }
    }
    if (result) {
        ares_freeaddrinfo(result);
    }
    state->pending--;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL || server_csv[0] == '\0') {
        return 0;
    }

    // Parse fuzz input: first byte determines number of lookups (1..MAX_LOOKUPS)
    size_t num_lookups = (data[0] % MAX_LOOKUPS) + 1;
    if (size < 1 + num_lookups) {
        return 0;
    }

    // Extract hostnames from fuzz input, each as a null-terminated string
    char hostnames[MAX_LOOKUPS][MAX_HOSTNAME_LEN];
    size_t offset = 1;
    for (size_t i = 0; i < num_lookups; i++) {
        size_t len = data[offset];
        offset++;
        if (offset + len > size) {
            return 0;
        }
        if (len >= MAX_HOSTNAME_LEN) {
            len = MAX_HOSTNAME_LEN - 1;
        }
        memcpy(hostnames[i], data + offset, len);
        hostnames[i][len] = '\0';
        offset += len;
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

    lookup_state state;
    memset(&state, 0, sizeof(state));
    state.channel = channel;
    state.pending = 0;
    state.total = 0;
    state.failures = 0;

    for (size_t i = 0; i < num_lookups; i++) {
        struct ares_addrinfo_hints hints;
        memset(&hints, 0, sizeof(hints));
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;

        ares_getaddrinfo(channel, hostnames[i], NULL, &hints, dns_callback, &state);
        state.pending++;
        state.total++;
    }

    // Process events until all lookups complete or timeout
    int max_waits = 100;
    while (state.pending > 0 && max_waits-- > 0) {
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 10000; // 10ms
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        ares_process(channel, &tv);
    }

    ares_destroy(channel);
    return 0;
}