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
    if (size < 2) {
        return 0;
    }

    /* Derive a bounded timeout from the first two bytes */
    unsigned int timeout_ms = ((unsigned int)data[0] << 8) | data[1];
    timeout_ms = timeout_ms % 10000; /* bound to 0-9999 ms */

    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.timeout = timeout_ms;
    options.tries = 1;

    ares_channel channel;
    int status = ares_init_options(&channel, &options, ARES_OPT_TIMEOUT | ARES_OPT_TRIES);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv) {
        ares_set_servers_csv(channel, server_csv);
    }

    /* Use a fixed hostname for the lookup */
    const char *host = "example.com";

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, host, NULL, &hints, getaddrinfo_callback, NULL);

    /* Process events for a bounded time */
    int max_wait_ms = 5000;
    int waited = 0;
    while (waited < max_wait_ms) {
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
        tv.tv_usec = 100000; /* 100 ms */
        int sel = select(nfds, &read_fds, &write_fds, NULL, &tv);
        if (sel < 0) {
            break;
        }
        ares_process(channel, &read_fds, &write_fds);
        waited += 100;
    }

    ares_destroy(channel);
    return 0;
}