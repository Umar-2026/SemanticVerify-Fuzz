#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ares.h>

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    int *done = (int *)arg;
    (void)timeouts;
    if (status == ARES_SUCCESS && result) {
        ares_freeaddrinfo(result);
    }
    *done = 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv || !server_csv[0]) {
        return 0;
    }

    ares_channel_t *channel1 = NULL;
    ares_channel_t *channel2 = NULL;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;

    if (ares_init_options(&channel1, &options, 0) != ARES_SUCCESS) {
        return 0;
    }
    if (ares_init_options(&channel2, &options, 0) != ARES_SUCCESS) {
        ares_destroy(channel1);
        return 0;
    }

    if (ares_set_servers_csv(channel1, server_csv) != ARES_SUCCESS) {
        ares_destroy(channel2);
        ares_destroy(channel1);
        return 0;
    }
    if (ares_set_servers_csv(channel2, server_csv) != ARES_SUCCESS) {
        ares_destroy(channel2);
        ares_destroy(channel1);
        return 0;
    }

    // Build a hostname from fuzz input, bounded to reasonable length.
    char hostname[256];
    size_t len = size < sizeof(hostname) - 1 ? size : sizeof(hostname) - 1;
    memcpy(hostname, data, len);
    hostname[len] = '\0';
    // Ensure it's a valid C string (no embedded NULs from fuzz input).
    for (size_t i = 0; i < len; i++) {
        if (hostname[i] == '\0') {
            hostname[i] = 'a';
        }
    }

    int done1 = 0;
    int done2 = 0;
    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel1, hostname, NULL, &hints, callback, &done1);
    ares_getaddrinfo(channel2, hostname, NULL, &hints, callback, &done2);

    // Process both channels until both callbacks fire or timeout.
    int max_fd = -1;
    fd_set read_fds, write_fds, except_fds;
    struct timeval tv;
    int nfds;
    int both_done = 0;
    int iterations = 0;
    while (!both_done && iterations < 1000) {
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        FD_ZERO(&except_fds);
        nfds = 0;

        ares_fds(channel1, &read_fds, &write_fds);
        ares_fds(channel2, &read_fds, &write_fds);

        max_fd = -1;
        for (int fd = 0; fd < FD_SETSIZE; fd++) {
            if (FD_ISSET(fd, &read_fds) || FD_ISSET(fd, &write_fds) || FD_ISSET(fd, &except_fds)) {
                if (fd > max_fd) max_fd = fd;
            }
        }

        tv.tv_sec = 0;
        tv.tv_usec = 10000; // 10ms
        if (max_fd >= 0) {
            if (select(max_fd + 1, &read_fds, &write_fds, &except_fds, &tv) < 0) {
                break;
            }
        } else {
            // No fds, just sleep a bit.
            struct timespec ts = {0, 10000000};
            nanosleep(&ts, NULL);
        }

        ares_process_fds(channel1, &read_fds, &write_fds);
        ares_process_fds(channel2, &read_fds, &write_fds);

        if (done1 && done2) {
            both_done = 1;
        }
        iterations++;
    }

    ares_destroy(channel2);
    ares_destroy(channel1);
    return 0;
}