#include <ares.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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
    if (status == ARES_SUCCESS) {
        if (result) {
            ares_freeaddrinfo(result);
        }
    }
}

int LLVMFuzzerTestOneInput(const unsigned char *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    /* Derive bounded timeout from first 4 bytes (0-1000 ms) */
    unsigned int timeout_ms = (data[0] | (data[1] << 8) | (data[2] << 16) | (data[3] << 24)) % 1001;

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.timeout = (int)timeout_ms;
    options.tries = 1;

    int status = ares_init_options(&channel, &options, ARES_OPT_TIMEOUT | ARES_OPT_TRIES);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv && server_csv[0] != '\0') {
        status = ares_set_servers_csv(channel, server_csv);
        if (status != ARES_SUCCESS) {
            ares_destroy(channel);
            return 0;
        }
    }

    /* Use a fixed hostname for the lookup */
    const char *hostname = "example.com";

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, getaddrinfo_callback, NULL);

    /* Process events for up to 2 seconds */
    int total_wait = 0;
    while (total_wait < 2000) {
        fd_set read_fds, write_fds;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        int nfds = 0;
        ares_fds(channel, &read_fds, &write_fds);
        nfds = ares_getsock(channel, NULL, 0);
        if (nfds == 0) {
            break;
        }
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 100000; /* 100 ms */
        int sel_ret = select(nfds, &read_fds, &write_fds, NULL, &tv);
        if (sel_ret < 0) {
            break;
        }
        ares_process_fds(channel, &read_fds, &write_fds);
        total_wait += 100;
    }

    ares_destroy(channel);
    return 0;
}