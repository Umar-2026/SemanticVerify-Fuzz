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
    if (size < 1) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv || server_csv[0] == '\0') {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;

    if (ares_init_options(&channel, &options, 0) != ARES_SUCCESS) {
        return 0;
    }

    if (ares_set_servers_csv(channel, server_csv) != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    /* Derive a bounded hostname from fuzz input. */
    char hostname[256];
    size_t len = size < sizeof(hostname) - 1 ? size : sizeof(hostname) - 1;
    memcpy(hostname, data, len);
    hostname[len] = '\0';

    /* Ensure the hostname is NUL-terminated and printable-ish. */
    for (size_t i = 0; i < len; i++) {
        if (hostname[i] == '\0' || hostname[i] == '\n' || hostname[i] == '\r') {
            hostname[i] = '.';
        }
    }

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, getaddrinfo_callback, NULL);

    /* Run the event loop with a bounded timeout. */
    int nfds;
    fd_set readers, writers;
    struct timeval tv, *tvp;
    int total_wait_ms = 0;
    const int max_wait_ms = 5000;

    while (total_wait_ms < max_wait_ms) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        nfds = ares_fds(channel, &readers, &writers);
        if (nfds == 0) {
            break;
        }
        tv.tv_sec = 0;
        tv.tv_usec = 100000; /* 100 ms */
        tvp = &tv;
        if (select(nfds, &readers, &writers, NULL, tvp) < 0) {
            break;
        }
        ares_process(channel, &readers, &writers);
        total_wait_ms += 100;
    }

    ares_destroy(channel);
    return 0;
}