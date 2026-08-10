#include <ares.h>
#include <ares_version.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#endif

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    (void)arg;
    (void)timeouts;
    if (status == ARES_SUCCESS && result) {
        struct ares_addrinfo_node *node = result->nodes;
        while (node) {
            if (node->ai_family == AF_INET) {
                struct sockaddr_in *sa = (struct sockaddr_in *)node->ai_addr;
                char buf[INET_ADDRSTRLEN];
                if (inet_ntop(AF_INET, &sa->sin_addr, buf, sizeof(buf))) {
                    /* consume result */
                }
            } else if (node->ai_family == AF_INET6) {
                struct sockaddr_in6 *sa6 = (struct sockaddr_in6 *)node->ai_addr;
                char buf[INET6_ADDRSTRLEN];
                if (inet_ntop(AF_INET6, &sa6->sin6_addr, buf, sizeof(buf))) {
                    /* consume result */
                }
            }
            node = node->ai_next;
        }
    }
    if (result) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    int optmask = ARES_OPT_FLAGS;

    int status = ares_init_options(&channel, &options, optmask);
    if (status != ARES_SUCCESS) return 0;

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv && server_csv[0]) {
        ares_set_servers_csv(channel, server_csv);
    }

    /* Derive a hostname from fuzz input, bounded length */
    size_t name_len = data[0] % 64;
    if (name_len > size - 1) name_len = size - 1;
    char hostname[65];
    memcpy(hostname, data + 1, name_len);
    hostname[name_len] = '\0';

    /* Ensure hostname is printable-ish and not empty */
    for (size_t i = 0; i < name_len; i++) {
        if (hostname[i] < 0x20 || hostname[i] > 0x7e) {
            hostname[i] = 'a' + (hostname[i] % 26);
        }
    }
    if (name_len == 0) {
        strcpy(hostname, "localhost");
    }

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, callback, NULL);

    /* Pump the event loop with a bounded number of iterations */
    int max_fd = 0;
    fd_set read_fds, write_fds;
    struct timeval tv;
    for (int iter = 0; iter < 100; iter++) {
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        tv.tv_sec = 0;
        tv.tv_usec = 1000;
        ares_fds(channel, &read_fds, &write_fds);
        if (ares_getsock(channel, NULL, 0) == 0) break;
        int n = select(max_fd + 1, &read_fds, &write_fds, NULL, &tv);
        if (n < 0) break;
        ares_process(channel, &read_fds, &write_fds);
    }

    ares_destroy(channel);
    return 0;
}