#include <ares.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif

static void sleep_ms(int ms) {
#ifdef _WIN32
    Sleep(ms);
#else
    usleep(ms * 1000);
#endif
}

static void getaddrinfo_callback(void *arg, int status, struct ares_addrinfo *result) {
    (void)arg;
    if (status == ARES_SUCCESS && result) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));

    /* Derive a bounded timeout (1-1000 ms) from the first 4 bytes */
    uint32_t timeout_ms = (uint32_t)data[0] | ((uint32_t)data[1] << 8) |
                          ((uint32_t)data[2] << 16) | ((uint32_t)data[3] << 24);
    timeout_ms = (timeout_ms % 1000) + 1;

    options.timeout = (int)timeout_ms;
    options.flags = ARES_FLAG_STAYOPEN;

    int status = ares_init_options(&channel, &options, ARES_OPT_TIMEOUT | ARES_OPT_FLAGS);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    /* Configure DNS server from environment variable */
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv) {
        status = ares_set_servers_csv(channel, server_csv);
        if (status != ARES_SUCCESS) {
            ares_destroy(channel);
            return 0;
        }
    }

    /* Use remaining fuzz bytes to construct a hostname (bounded length) */
    size_t host_len = size - 4;
    if (host_len > 255) {
        host_len = 255;
    }
    char hostname[256];
    memcpy(hostname, data + 4, host_len);
    hostname[host_len] = '\0';

    /* Perform address lookup */
    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, getaddrinfo_callback, NULL);

    /* Process events until callback completes or timeout */
    int max_waits = 100;
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
        tv.tv_usec = 10000; /* 10 ms */
        if (select(nfds, &read_fds, &write_fds, NULL, &tv) < 0) {
            break;
        }
        ares_process(channel, &read_fds, &write_fds);
    }

    ares_destroy(channel);
    return 0;
}