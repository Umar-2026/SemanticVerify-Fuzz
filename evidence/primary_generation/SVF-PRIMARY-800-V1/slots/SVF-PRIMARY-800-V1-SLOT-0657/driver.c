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

static void addr_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    uint32_t *summary = (uint32_t *)arg;
    if (status != ARES_SUCCESS || result == NULL) {
        return;
    }
    struct ares_addrinfo_node *node = result->nodes;
    while (node != NULL) {
        if (node->ai_family == AF_INET && node->ai_addrlen >= sizeof(struct sockaddr_in)) {
            struct sockaddr_in *sin = (struct sockaddr_in *)node->ai_addr;
            *summary += (uint32_t)ntohl(sin->sin_addr.s_addr);
        } else if (node->ai_family == AF_INET6 && node->ai_addrlen >= sizeof(struct sockaddr_in6)) {
            struct sockaddr_in6 *sin6 = (struct sockaddr_in6 *)node->ai_addr;
            const uint8_t *b = (const uint8_t *)&sin6->sin6_addr;
            for (int i = 0; i < 16; i++) {
                *summary += b[i];
            }
        }
        node = node->ai_next;
    }
    ares_freeaddrinfo(result);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL) {
        server_csv = "127.0.0.1";
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

    // Use fuzz data to construct a hostname (bounded length)
    size_t host_len = data[0] % 64;
    if (host_len > size - 1) {
        host_len = size - 1;
    }
    char hostname[65];
    memcpy(hostname, data + 1, host_len);
    hostname[host_len] = '\0';

    uint32_t summary = 0;
    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, addr_callback, &summary);

    // Process events until the callback completes or a bounded number of iterations
    int max_iter = 1000;
    while (max_iter-- > 0) {
        int nfds;
        fd_set read_fds, write_fds;
        struct timeval tv;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) {
            break;
        }
        tv.tv_sec = 0;
        tv.tv_usec = 1000;
        if (select(nfds, &read_fds, &write_fds, NULL, &tv) < 0) {
            break;
        }
        ares_process(channel, &read_fds, &write_fds);
    }

    ares_destroy(channel);
    return 0;
}