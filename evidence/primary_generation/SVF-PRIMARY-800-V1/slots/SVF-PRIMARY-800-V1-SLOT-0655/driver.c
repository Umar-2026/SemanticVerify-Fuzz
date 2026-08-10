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
    uint32_t *sum = (uint32_t *)arg;
    if (status != ARES_SUCCESS || result == NULL) {
        return;
    }
    struct ares_addrinfo_node *node = result->nodes;
    while (node != NULL) {
        if (node->ai_family == AF_INET) {
            struct sockaddr_in *sin = (struct sockaddr_in *)node->ai_addr;
            const unsigned char *b = (const unsigned char *)&sin->sin_addr;
            *sum += ((uint32_t)b[0] << 24) | ((uint32_t)b[1] << 16) | ((uint32_t)b[2] << 8) | b[3];
        } else if (node->ai_family == AF_INET6) {
            struct sockaddr_in6 *sin6 = (struct sockaddr_in6 *)node->ai_addr;
            const unsigned char *b = (const unsigned char *)&sin6->sin6_addr;
            for (int i = 0; i < 16; i++) {
                *sum += b[i];
            }
        }
        node = node->ai_next;
    }
    ares_freeaddrinfo(result);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    // Use first byte to select a hostname length, bounded.
    size_t hostlen = data[0] % 64;
    if (size < 1 + hostlen) return 0;

    char hostname[65];
    memcpy(hostname, data + 1, hostlen);
    hostname[hostlen] = '\0';

    // Ensure the hostname is a valid C string (no embedded NULs).
    for (size_t i = 0; i < hostlen; i++) {
        if (hostname[i] == '\0') {
            hostname[i] = 'a';
        }
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL) {
        server_csv = "127.0.0.1";
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    options.timeout = 2000;
    options.tries = 1;

    int rc = ares_init_options(&channel, &options, ARES_OPT_FLAGS | ARES_OPT_TIMEOUT | ARES_OPT_TRIES);
    if (rc != ARES_SUCCESS) {
        return 0;
    }

    rc = ares_set_servers_csv(channel, server_csv);
    if (rc != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    uint32_t sum = 0;
    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, callback, &sum);

    // Process events for a bounded time (e.g., up to 1000 iterations or 2 seconds).
    int max_waits = 1000;
    while (max_waits-- > 0) {
        fd_set read_fds, write_fds;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        int nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) {
            break;
        }
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 2000; // 2 ms
        if (select(nfds, &read_fds, &write_fds, NULL, &tv) < 0) {
            break;
        }
        ares_process(channel, &read_fds, &write_fds);
    }

    ares_destroy(channel);
    return 0;
}