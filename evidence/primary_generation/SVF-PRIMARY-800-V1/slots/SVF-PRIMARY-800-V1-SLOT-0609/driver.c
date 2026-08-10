#include <ares.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    (void)arg;
    (void)status;
    (void)timeouts;
    if (result) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv) {
        return 0;
    }

    ares_channel_t *channel = NULL;
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

    // Derive a bounded hostname from fuzz input.
    // Use at most 255 bytes, ensure NUL termination.
    size_t host_len = size - 1;
    if (host_len > 255) {
        host_len = 255;
    }
    char *hostname = (char *)malloc(host_len + 1);
    if (!hostname) {
        ares_destroy(channel);
        return 0;
    }
    memcpy(hostname, data, host_len);
    hostname[host_len] = '\0';

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, callback, NULL);

    // Process events until the callback is invoked or a bounded time.
    // Use a simple loop with ares_process_fd.
    int nfds;
    ares_socket_t sockets[ARES_GETSOCK_MAXNUM];
    int bits = ares_getsock(channel, sockets, ARES_GETSOCK_MAXNUM);
    for (int i = 0; i < ARES_GETSOCK_MAXNUM; i++) {
        if (bits & (1 << i)) {
            // Not a real poll; just call process with the socket.
            ares_process_fd(channel, sockets[i], sockets[i]);
        }
    }
    // Also process with no fds to handle timeouts.
    ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);

    ares_destroy(channel);
    free(hostname);
    return 0;
}