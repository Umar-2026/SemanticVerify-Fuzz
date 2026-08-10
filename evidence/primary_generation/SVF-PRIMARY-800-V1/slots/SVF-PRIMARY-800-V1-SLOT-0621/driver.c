#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

#ifdef __cplusplus
extern "C" {
#endif

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    ares_channel_t *channel = NULL;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    int optmask = ARES_OPT_FLAGS;

    int status = ares_init_options(&channel, &options, optmask);
    if (status != ARES_SUCCESS) return 0;

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL) {
        ares_destroy(channel);
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    // Derive a bounded domain name from fuzz input.
    // Use up to 63 bytes for the name, ensure null termination.
    size_t name_len = size < 64 ? size : 63;
    char name[64];
    memcpy(name, data, name_len);
    name[name_len] = '\0';

    // Ensure the name is not empty and does not contain invalid characters.
    if (name[0] == '\0') {
        ares_destroy(channel);
        return 0;
    }

    // Issue a single A-record query.
    ares_query_dnsrec(channel, name, ARES_CLASS_IN, ARES_REC_TYPE_A, NULL, NULL, NULL);

    // Process events for a bounded time to allow the callback to fire.
    // Use a simple loop with a timeout.
    int max_fd = 0;
    fd_set read_fds, write_fds;
    struct timeval tv;
    for (int i = 0; i < 10; i++) {
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        ares_fds(channel, &read_fds, &write_fds);
        if (ares_getsock(channel, NULL, 0) == 0) break; // no sockets
        tv.tv_sec = 0;
        tv.tv_usec = 10000; // 10 ms
        select(max_fd + 1, &read_fds, &write_fds, NULL, &tv);
        ares_process_fd(channel, FD_ISSET(0, &read_fds) ? 0 : ARES_SOCKET_BAD,
                        FD_ISSET(1, &write_fds) ? 1 : ARES_SOCKET_BAD);
    }

    ares_destroy(channel);
    return 0;
}

#ifdef __cplusplus
}
#endif