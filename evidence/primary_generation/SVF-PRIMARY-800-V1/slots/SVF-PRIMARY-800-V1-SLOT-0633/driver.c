#include <ares.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#endif

#define MAX_LOOKUPS 16
#define MAX_NAME_LEN 256

typedef struct {
    int pending;
    int completed;
    int errors;
} lookup_state;

static void addr_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    lookup_state *state = (lookup_state *)arg;
    state->completed++;
    if (status != ARES_SUCCESS) {
        state->errors++;
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
            if (addr[0]) {
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
    if (size == 0) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL || server_csv[0] == '\0') {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    int optmask = ARES_OPT_FLAGS;

    int status = ares_init_options(&channel, &options, optmask);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    lookup_state state;
    state.pending = 0;
    state.completed = 0;
    state.errors = 0;

    size_t offset = 0;
    int lookups = 0;
    while (offset < size && lookups < MAX_LOOKUPS) {
        size_t name_len = data[offset++];
        if (name_len == 0 || name_len > MAX_NAME_LEN - 1) {
            break;
        }
        if (offset + name_len > size) {
            break;
        }
        char name[MAX_NAME_LEN];
        memcpy(name, data + offset, name_len);
        name[name_len] = '\0';
        offset += name_len;

        struct ares_addrinfo_hints hints;
        memset(&hints, 0, sizeof(hints));
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;

        state.pending++;
        ares_getaddrinfo(channel, name, NULL, &hints, addr_callback, &state);
        lookups++;
    }

    if (lookups == 0) {
        ares_destroy(channel);
        return 0;
    }

    int numfds;
    fd_set readers, writers;
    struct timeval tv, *tvp;
    while (state.pending > 0) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        numfds = ares_fds(channel, &readers, &writers);
        if (numfds == 0) {
            break;
        }
        tv.tv_sec = 1;
        tv.tv_usec = 0;
        tvp = &tv;
        if (select(numfds, &readers, &writers, NULL, tvp) < 0) {
            break;
        }
        ares_process(channel, &readers, &writers);
    }

    ares_destroy(channel);
    return 0;
}