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
    int *summary = (int *)arg;
    struct ares_addrinfo_node *node;

    if (status != ARES_SUCCESS || result == NULL) {
        if (summary != NULL) {
            *summary = -1;
        }
        if (result != NULL) {
            ares_freeaddrinfo(result);
        }
        return;
    }

    if (summary != NULL) {
        *summary = 0;
    }

    for (node = result->nodes; node != NULL; node = node->ai_next) {
        if (node->ai_family == AF_INET) {
            if (summary != NULL) {
                (*summary)++;
            }
        } else if (node->ai_family == AF_INET6) {
            if (summary != NULL) {
                (*summary) += 1000;
            }
        }
    }

    ares_freeaddrinfo(result);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    ares_channel channel;
    struct ares_options options;
    int optmask = 0;
    int status;
    const char *server_csv;
    char *hostname;
    size_t hostname_len;
    int summary = 0;
    struct ares_addrinfo_hints hints;

    if (size < 1) {
        return 0;
    }

    server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL) {
        server_csv = "127.0.0.1";
    }

    memset(&options, 0, sizeof(options));
    optmask = ARES_OPT_FLAGS;
    options.flags = ARES_FLAG_STAYOPEN;

    status = ares_init_options(&channel, &options, optmask);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    hostname_len = size;
    if (hostname_len > 255) {
        hostname_len = 255;
    }
    hostname = (char *)malloc(hostname_len + 1);
    if (hostname == NULL) {
        ares_destroy(channel);
        return 0;
    }
    memcpy(hostname, data, hostname_len);
    hostname[hostname_len] = '\0';

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, addr_callback, &summary);

    /* Process events until the callback has been invoked or a bounded time. */
    for (int i = 0; i < 100; i++) {
        struct timeval tv;
        fd_set read_fds, write_fds;
        int nfds;

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
    free(hostname);

    return 0;
}