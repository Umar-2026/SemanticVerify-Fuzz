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
    if (status == ARES_SUCCESS && result != NULL) {
        ares_freeaddrinfo(result);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
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

    int status = ares_init_options(&channel, &options, ARES_OPT_FLAGS | ARES_OPT_TIMEOUT | ARES_OPT_TRIES);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    size_t name_len = size - 1;
    char *name = (char *)malloc(name_len + 1);
    if (name == NULL) {
        ares_destroy(channel);
        return 0;
    }
    memcpy(name, data, name_len);
    name[name_len] = '\0';

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, name, NULL, &hints, getaddrinfo_callback, NULL);

    int num_fds = 0;
    fd_set read_fds, write_fds;
    struct timeval tv;
    int max_fd = -1;

    for (int i = 0; i < 10; i++) {
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        tv.tv_sec = 0;
        tv.tv_usec = 200000;

        num_fds = ares_fds(channel, &read_fds, &write_fds);
        if (num_fds == 0) {
            break;
        }

        max_fd = -1;
        for (int fd = 0; fd < FD_SETSIZE; fd++) {
            if (FD_ISSET(fd, &read_fds) || FD_ISSET(fd, &write_fds)) {
                max_fd = fd;
            }
        }

        if (max_fd >= 0) {
            select(max_fd + 1, &read_fds, &write_fds, NULL, &tv);
            ares_process(channel, &read_fds, &write_fds);
        } else {
            sleep_ms(10);
        }
    }

    free(name);
    ares_destroy(channel);
    return 0;
}