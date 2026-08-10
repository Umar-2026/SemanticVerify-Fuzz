#include <ares.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>

static int callback_called = 0;
static int callback_status = -1;
static int callback_timeouts = 0;
static struct ares_addrinfo *callback_result = NULL;

static void addr_callback(void *arg, int status, int timeouts, struct ares_addrinfo *res) {
    (void)arg;
    callback_called = 1;
    callback_status = status;
    callback_timeouts = timeouts;
    callback_result = res;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    ares_channel channel;
    struct ares_options options;
    int optmask = 0;
    int status;
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    char hostname[256];
    size_t hostname_len;
    struct ares_addrinfo_hints hints;
    int fd_count;
    fd_set read_fds, write_fds;
    struct timeval tv;
    int nfds;
    int i;
    int result = 0;

    if (size < 1) return 0;

    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    optmask |= ARES_OPT_FLAGS;

    status = ares_init_options(&channel, &options, optmask);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    if (server_csv != NULL && server_csv[0] != '\0') {
        status = ares_set_servers_csv(channel, server_csv);
        if (status != ARES_SUCCESS) {
            ares_destroy(channel);
            return 0;
        }
    }

    hostname_len = size < sizeof(hostname) - 1 ? size : sizeof(hostname) - 1;
    memcpy(hostname, data, hostname_len);
    hostname[hostname_len] = '\0';

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    callback_called = 0;
    callback_status = -1;
    callback_timeouts = 0;
    callback_result = NULL;

    ares_getaddrinfo(channel, hostname, NULL, &hints, addr_callback, NULL);

    for (i = 0; i < 100 && !callback_called; i++) {
        fd_count = ares_fds(channel, &read_fds, &write_fds);
        if (fd_count == 0) {
            break;
        }
        tv.tv_sec = 0;
        tv.tv_usec = 10000;
        nfds = select(fd_count, &read_fds, &write_fds, NULL, &tv);
        if (nfds < 0) {
            if (errno == EINTR) continue;
            break;
        }
        ares_process(channel, &read_fds, &write_fds);
    }

    if (callback_called) {
        if (callback_status == ARES_SUCCESS && callback_result != NULL) {
            result = 1;
        } else if (callback_status == ARES_ENOTFOUND || callback_status == ARES_ENODATA) {
            result = 2;
        } else if (callback_status == ARES_ETIMEOUT) {
            result = 3;
        } else {
            result = 4;
        }
    } else {
        result = 5;
    }

    if (callback_result != NULL) {
        ares_freeaddrinfo(callback_result);
    }

    ares_destroy(channel);
    return result;
}