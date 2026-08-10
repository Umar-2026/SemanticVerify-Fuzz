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
#define MAX_HOSTNAME_LEN 256

typedef struct {
    int pending;
    int completed;
    int failures;
} lookup_state;

static void dns_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    lookup_state *state = (lookup_state *)arg;
    state->completed++;
    if (status != ARES_SUCCESS) {
        state->failures++;
    }
    if (result) {
        ares_freeaddrinfo(result);
    }
    state->pending--;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv || server_csv[0] == '\0') {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    int optmask = 0;

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    if (ares_set_servers_csv(channel, server_csv) != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    lookup_state state;
    state.pending = 0;
    state.completed = 0;
    state.failures = 0;

    size_t offset = 0;
    int lookups = 0;

    while (offset < size && lookups < MAX_LOOKUPS) {
        size_t len = data[offset];
        offset++;
        if (len == 0 || len > MAX_HOSTNAME_LEN || offset + len > size) {
            break;
        }

        char hostname[MAX_HOSTNAME_LEN + 1];
        memcpy(hostname, data + offset, len);
        hostname[len] = '\0';
        offset += len;

        struct ares_addrinfo_hints hints;
        memset(&hints, 0, sizeof(hints));
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;

        state.pending++;
        ares_getaddrinfo(channel, hostname, NULL, &hints, dns_callback, &state);
        lookups++;
    }

    if (state.pending == 0) {
        ares_destroy(channel);
        return 0;
    }

    int numfds;
    fd_set readers, writers;
    struct timeval tv;
    int res;

    while (state.pending > 0) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        numfds = 0;
        ares_fds(channel, &readers, &writers);
        if (ares_getsock(channel, NULL, 0) == 0) {
            break;
        }
        tv.tv_sec = 0;
        tv.tv_usec = 100000;
        res = select(numfds, &readers, &writers, NULL, &tv);
        if (res < 0) {
            break;
        }
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        ares_process(channel, &readers, &writers);
    }

    ares_destroy(channel);
    return 0;
}