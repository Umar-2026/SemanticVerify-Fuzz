#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

#ifdef SVF_CARES_SERVER_CSV
static const char *server_csv = SVF_CARES_SERVER_CSV;
#else
static const char *server_csv = "127.0.0.1";
#endif

static void query_callback(void *arg, int status, int timeouts, unsigned char *abuf, int alen) {
    (void)arg;
    (void)status;
    (void)timeouts;
    (void)abuf;
    (void)alen;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    options.timeout = 2000;
    options.tries = 1;

    int status = ares_init_options(&channel, &options, ARES_OPT_FLAGS | ARES_OPT_TIMEOUT | ARES_OPT_TRIES);
    if (status != ARES_SUCCESS) return 0;

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    // Build a bounded hostname from fuzz input: up to 63 chars, alphanumeric and dots.
    char name[64];
    size_t n = size < 63 ? size : 63;
    for (size_t i = 0; i < n; i++) {
        unsigned char c = data[i];
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '.' || c == '-') {
            name[i] = (char)c;
        } else {
            name[i] = 'a';
        }
    }
    name[n] = '\0';

    ares_query_dnsrec(channel, name, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, NULL, NULL);

    // Process events for a bounded time.
    for (int i = 0; i < 10; i++) {
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 100000; // 100ms
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        // Actually, we need to wait for events; use ares_process with timeout.
        // Simulate a short wait.
        ares_process(channel, &tv);
    }

    ares_destroy(channel);
    return 0;
}