#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <ares.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/socket.h>

typedef struct {
    int done;
    int status;
    struct ares_addrinfo *result;
} callback_data_t;

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    callback_data_t *data = (callback_data_t *)arg;
    (void)timeouts;
    data->done = 1;
    data->status = status;
    data->result = result;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    options.timeout = 1000;
    options.tries = 1;

    int status = ares_init_options(&channel, &options, ARES_OPT_FLAGS | ARES_OPT_TIMEOUT | ARES_OPT_TRIES);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL || server_csv[0] == '\0') {
        ares_destroy(channel);
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    char hostname[256];
    size_t len = size < sizeof(hostname) - 1 ? size : sizeof(hostname) - 1;
    memcpy(hostname, data, len);
    hostname[len] = '\0';

    callback_data_t cb_data;
    memset(&cb_data, 0, sizeof(cb_data));

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, hostname, NULL, &hints, callback, &cb_data);

    int attempts = 0;
    while (!cb_data.done && attempts < 100) {
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 10000;
        fd_set read_fds, write_fds;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        int nfds = ares_fds(channel, &read_fds, &write_fds);
        if (nfds == 0) {
            break;
        }
        if (select(nfds, &read_fds, &write_fds, NULL, &tv) < 0) {
            break;
        }
        ares_process(channel, &read_fds, &write_fds);
        attempts++;
    }

    if (cb_data.result != NULL) {
        ares_freeaddrinfo(cb_data.result);
    }

    ares_destroy(channel);
    return 0;
}