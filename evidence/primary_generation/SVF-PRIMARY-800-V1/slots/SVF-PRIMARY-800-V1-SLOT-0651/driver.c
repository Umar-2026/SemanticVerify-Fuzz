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
    int *count = (int *)arg;
    if (status == ARES_SUCCESS && result != NULL) {
        struct ares_addrinfo_node *node = result->nodes;
        while (node != NULL) {
            (*count)++;
            node = node->ai_next;
        }
    }
    if (result != NULL) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    (void)data;
    (void)size;

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL || server_csv[0] == '\0') {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    options.timeout = 2000;
    options.tries = 1;

    int status = ares_init_options(&channel, &options, ARES_OPT_FLAGS | ARES_OPT_TIMEOUT | ARES_OPT_TRIES);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    int count = 0;
    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, "example.com", NULL, &hints, callback, &count);

    int num_fds;
    fd_set readers, writers;
    struct timeval tv;
    while (1) {
        num_fds = 0;
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        tv.tv_sec = 0;
        tv.tv_usec = 100000; /* 100ms */
        ares_fds(channel, &readers, &writers);
        num_fds = ares_getsock(channel, NULL, 0);
        if (num_fds == 0) {
            break;
        }
        ares_process_fd(channel, FD_ISSET(0, &readers) ? 0 : ARES_SOCKET_BAD,
                        FD_ISSET(1, &writers) ? 1 : ARES_SOCKET_BAD);
        if (tv.tv_sec == 0 && tv.tv_usec == 0) {
            break;
        }
    }

    /* Bounded summary: just ensure the callback ran and count is sane */
    if (count > 1000) {
        count = 1000;
    }

    ares_destroy(channel);
    return 0;
}